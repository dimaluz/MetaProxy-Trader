# -*- coding: utf-8 -*-
# mitmproxy addon: лог всех URL и сохранение JSON-подобных ответов
import json
import re
from datetime import datetime
from pathlib import Path
from mitmproxy import ctx

CONFIG = {
    # Папка для результатов (создастся рядом со скриптом)
    "out_dir": "Captured_JSON",
    # Фильтр по хостам (оставь пустым, чтобы ловить вообще всё)
    "host_substrings": ["metaquotes", "mt5", "mt4"],
    # Записывать лог всех URL
    "write_urls_log": True,
    # Писать дубликаты одинаковых тел ответов?
    "save_duplicates": False,
}

BASE_DIR = Path(__file__).parent / CONFIG["out_dir"]
URLS_LOG = BASE_DIR / "urls.log"
counter = 0
seen_hashes = set()

def load(l):
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG["write_urls_log"]:
        URLS_LOG.touch(exist_ok=True)
    ctx.log.info(f"🚀 JSON sniffer запущен. Папка: {BASE_DIR}")

def _match_host(url: str) -> bool:
    if not CONFIG["host_substrings"]:
        return True
    u = url.lower()
    return any(sub in u for sub in CONFIG["host_substrings"])

def _is_jsonish(text: str) -> bool:
    s = text.lstrip()
    if not s:
        return False
    if s[0] in "{[":
        # быстрый тест
        try:
            json.loads(text)
            return True
        except Exception:
            # может быть поломанным — тогда не сохраняем
            return False
    # иногда приходит как ")]}',\n{...}"
    if s.startswith(")]}',"):
        try:
            json.loads(s.split("\n", 1)[1])
            return True
        except Exception:
            return False
    return False

def _short_hash(b: bytes) -> str:
    try:
        import hashlib
        return hashlib.md5(b).hexdigest()[:10]
    except Exception:
        return f"len{len(b)}"

def response(flow):
    global counter

    req = flow.request
    resp = flow.response

    # Лог URL, статус, content-type
    ct = resp.headers.get("content-type", "")
    line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {resp.status_code} {ct} {req.method} {req.url}"
    ctx.log.info(line)
    if CONFIG["write_urls_log"]:
        with URLS_LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    # Хост не подходит под фильтр? – выходим
    if not _match_host(req.pretty_url):
        return

    # Попробуем получить текст (mitmproxy сам разожмет gzip/deflate)
    try:
        text = resp.get_text(strict=False)
    except Exception:
        # Бинарный ответ/не декодируется
        return

    if not text:
        return

    # Проверка "похоже на JSON?"
    if not _is_jsonish(text):
        return

    # Дедупликация по телу (необязательно)
    body_bytes = text.encode("utf-8", errors="ignore")
    if not CONFIG["save_duplicates"]:
        h = _short_hash(body_bytes)
        if h in seen_hashes:
            ctx.log.info(f"↩️  Пропущен дубликат JSON (hash={h})")
            return
        seen_hashes.add(h)

    # Безопасное имя файла: хост + путь укороченный
    safe_host = re.sub(r"[^a-zA-Z0-9.-]", "_", req.host or "unknown")
    safe_path = re.sub(r"[^a-zA-Z0-9._-]", "_", (req.path or "/"))[:80]
    counter += 1
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"resp_{counter:04d}_{ts}_{safe_host}{safe_path}.json"
    out_path = BASE_DIR / filename

    try:
        # красиво перезаписываем (удаляем возможный ")]}'," префикс)
        clean_text = text
        if clean_text.lstrip().startswith(")]}',"):
            clean_text = clean_text.split("\n", 1)[1]

        parsed = json.loads(clean_text)
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
        ctx.log.info(f"✅ JSON сохранён: {out_path.name} ({len(body_bytes)} байт)")
    except Exception as e:
        # если вдруг это всё-таки невалидный JSON — сохраним как сырой текст
        raw_path = out_path.with_suffix(".txt")
        with raw_path.open("w", encoding="utf-8", errors="ignore") as f:
            f.write(text)
        ctx.log.warn(f"⚠️ Не удалось распарсить JSON ({e}). Сохранён сырой ответ: {raw_path.name}")

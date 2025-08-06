#!/usr/bin/env python3
"""
MetaProxy-Trader Setup
Автоматизация извлечения списка брокеров MetaTrader 4 через Android эмулятор и MITM прокси
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="metaproxy-trader",
    version="1.1.0",
    author="MetaProxy-Trader Team",
    description="Extracting MetaTrader Platform Broker List using Android Emulator and MITM Proxy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/3rtha/MetaProxy-Trader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Emulators",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords="metatrader, automation, android, mitm, proxy, broker, trading",
    project_urls={
        "Bug Reports": "https://github.com/3rtha/MetaProxy-Trader/issues",
        "Source": "https://github.com/3rtha/MetaProxy-Trader",
    },
)
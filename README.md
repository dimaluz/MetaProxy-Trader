# MetaProxy-Trader
Extracting MetaTrader Platform Broker List using Android Emulator and MITM Proxy

The overall system architecture of our project is depicted below in Figure. It consists
of several key components.

![System Architecture](https://github.com/3rtha/MetaProxy-Trader/assets/126825143/f88cb935-f5e2-407e-b2b7-82aa8835c853)

Follow the below steps to get started:
1. Set Up Genymotion Android Emulator: Download and install Genymotion from their official website. Create a virtual device in Genymotion
with the desired Android version and specifications. Install the MetaTrader app on the virtual device using either Google Play Store or an
APK file.

2. Configure MITM Proxy Settings: Install and configure MITM
Proxy on your local machine. Download the MITM CA certificate and
adjust the proxy settings on the Genymotion emulator. Ensure that the
virtual Android emulator’s IP address and port match your computer’s
IP address and port.

 'mitmproxy -s Global_JSON_Response_Extractor.py'


4. 

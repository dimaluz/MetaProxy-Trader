# MetaProxy-Trader
Extracting MetaTrader Platform Broker List using Android Emulator and MITM Proxy

The scripting process is employed for automation, encompassing tasks such
as navigating and searching for all broker names within the Genymotion environment. The main objective is to extract a comprehensive list of brokers
along with their corresponding information. To achieve this, MITM (Man-in-the-Middle) techniques are employed. Specifically, a proxy certificate is installed
in the Genymotion environment. As the Appium automation script is executed,
the MITM proxy captures network traffic. Subsequently, the captured traffic
leads to the local storage of specific responses in the form of JSON files.

The overall system architecture of our project is depicted below in Figure. It consists
of several key components.

![System Architecture](https://github.com/3rtha/MetaProxy-Trader/assets/126825143/f88cb935-f5e2-407e-b2b7-82aa8835c853)

Follow the below steps to get started:
1. Set Up Genymotion Android Emulator: Download and install GenyMotion from their official website. Create a virtual device in Genymotion
with the desired Android version and specifications. Install the MetaTrader app on the virtual device using either the Google Play Store or an
APK file.

2. Configure MITM Proxy Settings: Install and configure MITM
Proxy on your local machine. Download the MITM CA certificate and
adjust the proxy settings on the Genymotion emulator. Ensure that the
virtual Android emulator’s IP address and port match your computer’s
IP address and port.

```
 mitmproxy -s Global_JSON_Response_Extractor.py
```
4. Initiate Appium Server: Install Appium on your machine using
npm or another method. Start the Appium server using the appium command in a terminal.

5. Use Appium Inspector to Begin Session: Open Appium Inspector, a tool that comes with Appium, in your web browser. Configure the
desired capabilities for your test session. This includes specifying the device, app package, app activity, etc. Start a session using the capabilities
you’ve configured.

Use the below Desired Capabilities and start the session:
```
For MT4 "platformName":
"Android", "appium:appPackage": "net.metaquotes.metatrader4",
"appium:appActivity": "net.metaquotes.metatrader4.ui.MainActivity",
"appium:app": "C:/Users/Downloads/MetaTrader4.apk"
```
6. Execute Automation Scripts: Write or use the provided automation scripts to interact with the MetaTrader app. Run the automation
scripts. These scripts can simulate user interactions, validate app behavior, and perform tasks within the app.
```
Automation MT4.py
```

7. Monitor and Analyze Results: Monitor the output and logs of
your automation scripts to ensure they are executing as expected. Inspect
the app’s behavior in the Genymotion emulator as the automation scripts
run. Use MITM Proxy to capture and analyze network traffic for debugging and testing purposes.

## Contributing
We welcome contributions from the community. If you have ideas for improvement or find any issues, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

## Acknowledgments
MetaTrader for providing valuable broker information.
Our open-source community for their support and contributions.



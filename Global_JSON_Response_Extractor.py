import os
import json
from mitmproxy import ctx

# user directory path
USER_DIRECTORY = "C:/Users/T. Bannikere/Desktop/IMDEA - MetaScam/Meta_Trader_brokers/MT5_brokers"

# Store responses in a dictionary with a counter
response_counter = 1

def response(flow):
    global response_counter
    
    # Filter requests based on your criteria
    if "updates.metaquotes.net/public/mt5/network/mobile" in flow.request.url:
        # Check if response content type is JSON
        if "application/json" in flow.response.headers.get("content-type", ""):
            try:
                # Parse the JSON content
                json_data = json.loads(flow.response.content)
                
                # Create a new JSON file for each response
                filename = f"response_{response_counter}.json"
                filepath = os.path.join(USER_DIRECTORY, filename)
                
                # Write the JSON data in a structured format to the file
                with open(filepath, "w") as f:
                    json.dump(json_data, f, indent=4)
                
                response_counter += 1
                ctx.log.info(f"JSON response {response_counter - 1} saved in user directory.")
            
            except json.JSONDecodeError:
                ctx.log.error("Error decoding JSON response.")
                pass


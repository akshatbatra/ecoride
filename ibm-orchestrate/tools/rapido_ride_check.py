from ibm_watsonx_orchestrate.agent_builder.tools import tool
import requests, json

AI_BROWSER_SERVER_URL=""

@tool(name='rapido_ride_check', description='a tool that call an AI browser server to extract rapido ride availability information')
def rapido_ride_check(source_location:str, destination_location:str):
    data = {
        "source_location": source_location,
        "destination_location": destination_location,
    }
    response = requests.post(f"{AI_BROWSER_SERVER_URL}/rapido_ride_check", data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to fetch rapido ride information"}
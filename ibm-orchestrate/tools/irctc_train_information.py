from ibm_watsonx_orchestrate.agent_builder.tools import tool
import requests, json

AI_BROWSER_SERVER_URL=""

@tool(name='irctc_train_information', description='a tool that call an AI browser server to extract IRCTC train schedule information from the internet')
def irctc_train_information(source_city:str, destination_city:str) -> str:
    data = {
        "source_city": source_city,
        "destination_city": destination_city,
    }
    response = requests.post(f"https://{AI_BROWSER_SERVER_URL}/train_information", data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to fetch train information"}
from ibm_watsonx_orchestrate.agent_builder.tools import tool
import requests, json
import os

@tool(name='buy_metro_ticket', description='a tool that uses a remote browser to visit a website to buy metro train ticket for commute')
def buy_metro_ticket(source_station:str, destination_station:str, email:str, mobile:str, upi_id:str):
    data = {
        "source_station": source_station,
        "destination_station": destination_station,
        "email": email,
        "mobile": mobile,
        "upi_id": upi_id
    }
    response = requests.post("https://ai-browser-server.fly.dev/buy_metro_ticket", data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to fetch train information"}
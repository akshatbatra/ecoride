from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from stagehand import Stagehand
from typing import List
import os

CDP_URL= os.getenv("CDP_URL") # CDP URL FOR REMOTE WEB BROWSER
print(os.getenv("WATSONX_URL"))
print(os.getenv("WATSONX_APIKEY"))
print(os.getenv("WATSONX_TOKEN"))
print(os.getenv("WATSONX_PROJECT_ID"))

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

class TrainInformationRequest(BaseModel):
    source_city: str
    destination_city: str

class TrainInformation(BaseModel):
    train_name: str
    train_number: str
    departure_time: str
    arrival_time: str
    duration: str

class TrainInfoList(BaseModel):
    Trains: List[TrainInformation]

@app.post("/train_information")
async def train_information(data: TrainInformationRequest):
    source_city = data.source_city
    destination_city = data.destination_city
    stagehand = Stagehand(
        env="LOCAL",
        model_name="watsonx/meta-llama/llama-3-2-90b-vision-instruct",
        local_browser_launch_options={
            "headless": True,
            "cdp_url": CDP_URL
        }
    )
    await stagehand.init()
    page = stagehand.page
    await page.goto(f"https://www.google.co.in/search?q=IRCTC%20trains%20from%20{source_city}%20to%20{destination_city}%20redbus.in")
    await page.wait_for_load_state("domcontentloaded")
    await page.act(f"Click on the first redbus.in link that isn't an advertisement")
    await page.wait_for_load_state("domcontentloaded")
    trains = await page.extract(
        "Extract the train_name, train_number, departure_time, arrival_time and duration information for every train", 
        schema=TrainInfoList
    )
    await stagehand.close()
    return {"trains": trains.model_dump_json()}


async def metro_ticket_buy(source_station, destination_station, email, mobile, upi_id):
    upi_parts = upi_id.split("@")
    upi_prefix = upi_parts[0] if len(upi_parts) > 0 else ""
    upi_suffix = upi_parts[1] if len(upi_parts) > 1 else ""

    stagehand = Stagehand(
        env="LOCAL",
        model_name="watsonx/meta-llama/llama-3-2-90b-vision-instruct",
        local_browser_launch_options={
            "headless": True,
            "cdp_url": CDP_URL
        }
    )
    await stagehand.init()
    page = stagehand.page
    await page.goto("https://easemytrip.com/metro")
    await page.wait_for_load_state("domcontentloaded")
    action = await page.observe(f"Select Delhi")
    await page.wait_for_load_state("domcontentloaded")
    await page.act(action[0])
    action = await page.observe("find the 'Depart From' dropdown to click, then find the 'Depart To' dropdown to click")
    await page.act(action[0])
    await page.act(f"click station most similar to '{source_station}' station in the opened dropdown")
    await page.act(action[1])
    await page.act(f"click station most similar to '{destination_station}' station in the opened dropdown")
    await page.act("click on continue booking")
    await page.wait_for_load_state("domcontentloaded")
    await page.act(f"find the email address field to click and enter {email} into that")
    await page.act(f"find the phone number field to click and enter {mobile} into that")
    await page.act("Click on continue booking")
    # await page.get_by_text("Verify & Pay").wait_for(state="attached")
    await page.act(f"find the UPI ID field to click and enter '{upi_prefix}' into that")
    if upi_suffix:
        await page.act(f"find the UPI bank suffix dropdown and to click and select '{upi_suffix}' from that")
    await page.get_by_text("Verify & Pay").click()
    await page.wait_for_load_state("domcontentloaded")
    await stagehand.close()

class MetroBookingRequest(BaseModel):
    source_station: str
    destination_station: str
    email: str
    mobile: str
    upi_id: str

@app.post("/buy_metro_ticket")
async def buy_metro_ticket(data: MetroBookingRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(metro_ticket_buy, data.source_station, data.destination_station, data.email, data.mobile, data.upi_id)
    return {"status": "success"}

class RapidoRideCheckRequest(BaseModel):
    source_location: str
    destination_location: str

@app.post("/rapido_ride_check")
async def rapido_ride_check(data: RapidoRideCheckRequest):
    source_location = data.source_location
    destination_location = data.destination_location

    stagehand = Stagehand(
        env="LOCAL",
        model_name="watsonx/meta-llama/llama-3-2-90b-vision-instruct",
        local_browser_launch_options={
            "headless": True,
            "cdp_url": CDP_URL
        }
    )

    await stagehand.init()
    page = stagehand.page
    await page.goto("https://www.rapido.bike/Home")
    await page.wait_for_load_state("domcontentloaded")
    await page.fill("input[aria-label='pickup']", source_location)
    await page.locator(".dropdown-item").is_visible()
    await page.locator(".dropdown-item > :first-child").first.click()
    await page.fill("input[aria-label='drop']", destination_location)
    await page.locator(".dropdown-item").is_visible()
    await page.locator(".dropdown-item > :first-child").first.click()
    await page.click("button[aria-label='book-ride']")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(3000)
    service_available = await page.locator(".select-service").count()
    is_service_available = (service_available > 0)
    await stagehand.close()
    return {"status": "Yes, rapido service available" if is_service_available else "No, rapido service unavailable"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, log_level="info")

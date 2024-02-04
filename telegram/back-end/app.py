# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# Allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],   
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client["ad_campaigns"]
collection = db["campaigns"]

class AdCampaignData(BaseModel):
    advertiserName: str
    productName: str
    campaignBriefs: str

@app.post("/get-data")
async def get_data(data: AdCampaignData):
    # Inserting the data into the database
    inserted_data = collection.insert_one(data.dict())
    inserted_id = str(inserted_data.inserted_id)
    
    # Retrieving the inserted document
    retrieved_data = collection.find_one({"_id": inserted_id})
    
    if retrieved_data:
        return retrieved_data
    else:
        raise HTTPException(status_code=404, detail="Data not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)

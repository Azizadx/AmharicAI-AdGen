# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
import requests

app = FastAPI()

# Allow requests from AiQim webapp 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["POST", "GET"],  # Allow both POST and GET methods
    allow_headers=["*"],
)
rag_end_point="http://localhost:8001"

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
        # Pass AdCampaignData instance directly to suggested_add endpoint
        return suggested_add(data)
    else:
        raise HTTPException(status_code=404, detail="Data not found")

@app.get("/suggested_add")
async def suggested_add(data: AdCampaignData):
    # Make request to RAG_ENDPOINT to get suggested ad
    rag_endpoint = rag_end_point
    params = {
        "advertiser": data.advertiserName,
        "product": data.productName,
        "brief": data.campaignBriefs
    }
    response = requests.get(rag_endpoint, params=params)
    if response.status_code == 200:
        return {"suggested_ad": response.json()}
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch suggested ad")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)

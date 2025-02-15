from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any website
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scraper import scrape_product

app = FastAPI()

# ✅ Add this to fix "Not Found" error at /
@app.get("/")
def home():
    return {"message": "Welcome to BulkBuy API! Visit /docs to test the API."}

class ProductRequest(BaseModel):
    url: str

@app.post("/scrape")
async def scrape_product_api(request: ProductRequest):
    try:
        data = scrape_product(request.url)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

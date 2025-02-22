from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scraper import scrape_product

app = FastAPI()

# ✅ Allow requests from specific domains (Shopify & API)
origins = [
    "https://your-shopify-store.myshopify.com",  # 🔹 Replace with your actual Shopify store URL
    "https://bulkbuy-api.onrender.com",  # 🔹 Your API's own domain
    "*",  # 🔹 Allows all domains (use with caution in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 👈 Allow Shopify to access your API
    allow_credentials=True,
    allow_methods=["*"],  # 👈 Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # 👈 Allow all headers
)

# ✅ Fix "Not Found" error at /
@app.get("/")
def home():
    return {"message": "Welcome to BulkBuy API! Visit /docs to test the API."}

# ✅ Define request body format
class ProductRequest(BaseModel):
    url: str

# ✅ Scraper endpoint
@app.post("/scrape")
async def scrape_product_api(request: ProductRequest):
    try:
        data = scrape_product(request.url)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

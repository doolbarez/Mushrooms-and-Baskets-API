from fastapi import FastAPI
from routers import mushrooms, baskets

app = FastAPI(title="Mushrooms and Baskets API")

app.include_router(mushrooms.router, prefix="/mushrooms", tags=["Mushrooms"])
app.include_router(baskets.router, prefix="/baskets", tags=["Baskets"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from fastapi import FastAPI
from app.routes import products
from app.background_tasks import start_background_updater
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Trendyol Ürün API", version="1.0.0")
app.include_router(products.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend'den gelen her isteğe izin verir, daha sonra bunu "http://localhost:5173" gibi daraltabilirsin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    start_background_updater()
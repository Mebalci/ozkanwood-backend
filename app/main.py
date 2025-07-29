from fastapi import FastAPI
from app.routes import products
from app.background_tasks import start_background_updater, start_simple_updater
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Özkan Wood API")

# Routes ekle
app.include_router(products.router, prefix="/api")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Uygulama başlatılırken çalışır"""
    print("🚀 Özkan Wood API başlatılıyor...")
    
    # Geliştirme için basit updater kullan
    start_simple_updater()
    
    # Prodüksyon için sürekli updater (isteğe bağlı)
    # start_background_updater()
    
    print("✅ API hazır!")

@app.get("/")
async def root():
    """Ana endpoint"""
    return {
        "message": "Özkan Wood API çalışıyor!",
        "endpoints": {
            "products": "/api/products",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Sağlık kontrolü"""
    return {"status": "healthy", "message": "API çalışıyor"}
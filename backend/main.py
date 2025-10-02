# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Assuming your endpoints are in a folder named 'api'
from api import simulation_endpoints, config_endpoints

app = FastAPI(
    title="VAJRA",
    description="Backend server for real-time drone swarm engagement simulation.",
    version="1.3.0" # Version bump for this specific fix
)

# --- A more robust CORS Policy ---
# This explicitly allows all common local development origins.
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API routers
app.include_router(simulation_endpoints.router)
app.include_router(config_endpoints.router)

@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint to check if the server is running."""
    return {"status": "success", "message": "Drone Swarm Simulation Server is running"}
# backend/main.py
from fastapi import FastAPI, Depends
from backend.itinerary_agent import generate_itinerary
from backend.memory_agent import MemoryAgent
from backend.optimization_agent import optimize_itinerary
from backend.weather_agent import get_weather
from backend.ollama_interface import OllamaInterface

app = FastAPI()

# Initialize agents
memory_agent = MemoryAgent()
ollama_interface = OllamaInterface()

@app.post("/collect_preferences/")
async def collect_preferences(city: str, start_time: str, end_time: str, budget: int, interests: list):
    # Store user preferences in memory
    memory_agent.store_preferences(city, start_time, end_time, budget, interests)
    return {"status": "Preferences collected"}

@app.post("/generate_itinerary/")
async def generate_initial_itinerary():
    preferences = memory_agent.get_preferences()
    itinerary = generate_itinerary(preferences)
    return {"itinerary": itinerary}

@app.post("/optimize_itinerary/")
async def optimize_user_itinerary(itinerary: dict):
    optimized_itinerary = optimize_itinerary(itinerary)
    return {"optimized_itinerary": optimized_itinerary}

@app.post("/get_weather/")
async def get_weather_info(city: str):
    weather_info = get_weather(city)
    return {"weather": weather_info}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

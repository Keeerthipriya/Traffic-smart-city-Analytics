from fastapi import FastAPI
from pydantic import BaseModel
from analysis import (
    load_data,
    peak_hours,
    junction_analysis,
    weather_analysis,
    get_best_route,
    get_worst_route
)

app = FastAPI(title="Traffic Smart Analytics API")


# -------------------------------
# Request Models (POST)
# -------------------------------
class TrafficInput(BaseModel):
    vehicle_count: int
    avg_speed: float


class RouteInput(BaseModel):
    junction_id: str


# -------------------------------
# Home route
# -------------------------------
@app.get("/")
def home():
    return {"message": "Traffic Analytics API is running"}


# -------------------------------
# GET: Full dataset
# -------------------------------
@app.get("/data")
def get_data():
    df = load_data()   # 🔥 load fresh data every time
    return df.to_dict(orient="records")


# -------------------------------
# GET: Peak hours
# -------------------------------
@app.get("/peak-hours")
def get_peak_hours():
    df = load_data()
    result = peak_hours(df)
    return result.reset_index().to_dict(orient="records")


# -------------------------------
# GET: Junction analysis
# -------------------------------
@app.get("/junction-analysis")
def get_junction_analysis():
    df = load_data()
    result = junction_analysis(df)
    return result.reset_index().to_dict(orient="records")


# -------------------------------
# GET: Weather analysis
# -------------------------------
@app.get("/weather-analysis")
def get_weather_analysis():
    df = load_data()
    result = weather_analysis(df)
    return result.reset_index().to_dict(orient="records")


# -------------------------------
# GET: Best route
# -------------------------------
@app.get("/best-route")
def best_route():
    df = load_data()
    result = get_best_route(df)
    return result.reset_index().to_dict(orient="records")


# -------------------------------
# GET: Worst route
# -------------------------------
@app.get("/worst-route")
def worst_route():
    df = load_data()
    result = get_worst_route(df)
    return result.reset_index().to_dict(orient="records")


# -------------------------------
# POST: Predict traffic level
# -------------------------------
@app.post("/predict")
def predict_traffic(input: TrafficInput):

    # Rule-based prediction
    if input.vehicle_count > 220 or input.avg_speed < 15:
        level = "High"
    elif input.vehicle_count > 150 or input.avg_speed < 30:
        level = "Medium"
    else:
        level = "Low"

    return {
        "vehicle_count": input.vehicle_count,
        "avg_speed": input.avg_speed,
        "traffic_level": level
    }


# -------------------------------
# POST: Route suggestion
# -------------------------------
@app.post("/route-suggestion")
def route_suggestion(input: RouteInput):
    df = load_data()

    filtered = df[df['junction_id'] == input.junction_id]

    if filtered.empty:
        return {"message": "No data found for this junction"}

    best = filtered.sort_values(
        by=["vehicle_count", "avg_speed"],
        ascending=[True, False]
    ).head(1)

    return best.to_dict(orient="records")
import pandas as pd



# -------------------------------
# Load and preprocess data
# -------------------------------
def load_data():
    df = pd.read_csv("dataset.csv")

    # Convert datetime
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Feature engineering
    df['hour'] = df['datetime'].dt.hour
    df['day_name'] = df['datetime'].dt.day_name()
    df['is_weekend'] = df['day_name'].isin(['Saturday', 'Sunday']).astype(int)

    # Apply rule-based traffic classification
    df['traffic_level'] = df.apply(get_traffic_level, axis=1)

    return df


# -------------------------------
# Rule-based traffic classification
# -------------------------------
def get_traffic_level(row):
    vehicle_count = row['vehicle_count']
    speed = row['avg_speed']

    # High congestion
    if vehicle_count > 220 or speed < 15:
        return "High"

    # Medium congestion
    elif 150 < vehicle_count <= 220 or 15 <= speed < 30:
        return "Medium"

    # Low congestion
    else:
        return "Low"


# -------------------------------
# Peak congestion hours
# -------------------------------
def peak_hours(df):
    result = df.groupby("hour")["vehicle_count"].mean().sort_values(ascending=False)
    return result


# -------------------------------
# Junction-wise analysis
# -------------------------------
def junction_analysis(df):
    result = df.groupby("junction_id")["vehicle_count"].mean().sort_values(ascending=False)
    return result


# -------------------------------
# Weather impact analysis
# -------------------------------
def weather_analysis(df):
    result = df.groupby("weather")["vehicle_count"].mean().sort_values(ascending=False)
    return result


# -------------------------------
# Best route suggestion (rule-based)
# -------------------------------
def best_routes(df):
    routes = df.groupby("junction_id").agg({
        "vehicle_count": "mean",
        "avg_speed": "mean"
    })

    # Rule:
    # Prefer LOW vehicle_count and HIGH speed
    routes = routes.sort_values(
        by=["vehicle_count", "avg_speed"],
        ascending=[True, False]
    )

    return routes


# -------------------------------
# Get best route (top recommendation)
# -------------------------------
def get_best_route(df):
    routes = best_routes(df)
    best = routes.head(1)
    return best


# -------------------------------
# Get worst route (most congested)
# -------------------------------
def get_worst_route(df):
    routes = best_routes(df)
    worst = routes.tail(1)
    return worst

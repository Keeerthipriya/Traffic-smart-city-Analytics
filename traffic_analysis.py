import pandas as pd
from utils.config import DATA_PATH

def load_data():
    df = pd.read_csv(DATA_PATH)

    # Convert datetime
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Feature engineering
    df['hour'] = df['datetime'].dt.hour
    df['day'] = df['datetime'].dt.day_name()

    # Traffic rule
    df['traffic_level'] = df.apply(get_traffic_level, axis=1)

    return df


def get_traffic_level(row):
    if row['avg_speed'] < 20 or row['vehicle_count'] > 200:
        return "High"
    elif row['avg_speed'] < 40:
        return "Medium"
    else:
        return "Low"


def peak_hours(df):
    return df.groupby("hour")["vehicle_count"].mean().sort_values(ascending=False)


def junction_analysis(df):
    return df.groupby("junction_id")["vehicle_count"].mean().sort_values(ascending=False)


def weather_analysis(df):
    return df.groupby("weather")["vehicle_count"].mean()


def best_routes(df):
    routes = df.groupby("junction_id").agg({
        "vehicle_count": "mean",
        "avg_speed": "mean"
    })

    routes = routes.sort_values(
        by=["vehicle_count", "avg_speed"],
        ascending=[True, False]
    )

    return routes

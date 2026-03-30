import pandas as pd

# 1. Load dataset
df = pd.read_csv("dataset.csv")

# 2. View basic info
print(df.head())
print(df.info())

# 3. Convert datetime column to proper format
df['datetime'] = pd.to_datetime(df['datetime'])

# 4. Extract useful time features
df['hour'] = df['datetime'].dt.hour
df['day'] = df['datetime'].dt.day
df['month'] = df['datetime'].dt.month

# (Optional but useful)
df['day_of_week_num'] = df['datetime'].dt.weekday  # Monday=0

# 5. Handle missing values
print(df.isnull().sum())

# If missing values exist:
df = df.dropna()   # simple method

# OR (better)
# df.fillna(method='ffill', inplace=True)

# 6. Remove duplicates
df = df.drop_duplicates()

# 7. Convert categorical columns to numeric

# Weather encoding
df['weather'] = df['weather'].map({
    'Clear': 0,
    'Cloudy': 1,
    'Rain': 2
})

# Day of week encoding (if string)
df['day_of_week'] = df['day_of_week'].map({
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6
})

# 8. Check final dataset
print(df.head())

# 9. Save cleaned dataset
df.to_csv("pre_processed_data.csv", index=False)
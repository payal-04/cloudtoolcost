import pandas as pd
from sklearn.linear_model import LinearRegression
from models.cost_model import daily

def predict_next_7_days():
    records = list(daily.find().sort("date_utc", 1))

    if len(records) < 5:
        return {"message": "Not enough data to predict"}

    df = pd.DataFrame(records)
    df["day"] = range(len(df))

    X = df[["day"]]
    y = df["amount"]

    model = LinearRegression()
    model.fit(X, y)

    future_days = [[len(df) + i] for i in range(7)]
    prediction = model.predict(future_days)

    return {
        "next_7_days_prediction": [round(p, 4) for p in prediction]
    }
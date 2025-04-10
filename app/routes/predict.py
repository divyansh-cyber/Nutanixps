from fastapi import APIRouter
from app.models.model_loader import model, scaler
from app.preprocessing.encoder import encode_features
from app.preprocessing.find import filter_flights
import pandas as pd

router = APIRouter()

@router.get("/predict")
def predict(source: str, dest:str, days:int):
    try:
        filter_flights(source, dest)
        print("Filtered flights based on source and destination.")

        encoded_row = encode_features(days)

        print("Feature encoding completed.")
        feature_columns = [
            "airline", "flight", "source_city", "departure_time", "stops",
            "arrival_time", "destination_city", "class", "duration", "days_left"
        ]

        X = encoded_row[feature_columns]
        X_scaled = scaler.transform(X)
        prediction = model.predict(X_scaled)

        df = pd.read_csv("available.csv")
        prices = []
        for i in prediction:
            prices.append(int(i))
            
        df["predicted_fare"] = prices
        df.to_csv("available.csv", index=False)

        return {"predicted_fare": prediction.tolist()[0:10]}

    except:
        return {"error": "An error occurred during prediction."}
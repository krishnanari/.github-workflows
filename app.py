from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import xgboost as xgb
import pandas as pd
from typing import Optional

# Create FastAPI instance
app = FastAPI()

# Load the trained XGBoost model
try:
    with open("xgb_model.pkl", "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    raise RuntimeError("The model file 'xgb_model.pkl' was not found. Please ensure it is in the correct path.")

# Define input schema using Pydantic
class InputData(BaseModel):
    user_id: int
    movie_id: int
    gender: Optional[int] = None
    occupation: Optional[int] = None
    age: Optional[int] = None
    release_year: Optional[int] = None
    release_month: Optional[int] = None

# Define the prediction endpoint
@app.post("/predict/")
def predict_rating(data: InputData):
    """
    Predict movie ratings based on input user and movie data.
    """
    try:
        # Prepare the input data as a DataFrame
        input_features = pd.DataFrame([{
            "user_id": data.user_id,
            "movie_id": data.movie_id,
            "gender": data.gender or 0,  # Replace None with default value 0
            "occupation": data.occupation or 0,
            "age": data.age or 0,
            "release_year": data.release_year or 0,
            "release_month": data.release_month or 0
        }])

        # Ensure features match the model's training format
        # Note: Replace 'model_features' with the actual list of feature names used during training
        model_features = ["user_id", "movie_id", "gender", "occupation", "age", "release_year", "release_month"]
        input_features = input_features[model_features]

        # Convert to DMatrix format for XGBoost prediction
        dmatrix = xgb.DMatrix(input_features)

        # Predict the rating
        predicted_rating = model.predict(dmatrix)

        # Return the result
        return {
            "user_id": data.user_id,
            "movie_id": data.movie_id,
            "predicted_rating": round(float(predicted_rating[0]), 2)  # Rounded to 2 decimals
        }

    except Exception as e:
        # Catch and return any errors
        return {"error": f"Prediction failed: {str(e)}"}

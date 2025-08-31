import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from train import train_model # Import the training function

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

# Initialize FastAPI app
app = FastAPI(title="Demand Forecast API")

# --- Model Loading ---
model_payload = None

def load_model():
    """Loads the model from disk into the global `model_payload`."""
    global model_payload
    if os.path.exists(MODEL_PATH):
        model_payload = joblib.load(MODEL_PATH)
        print("Model loaded successfully.")
    else:
        model_payload = None
        print("Model file not found. Train the model by calling the /train endpoint.")

# Load the model on application startup
load_model()

# --- Pydantic Models for Input/Output ---
class PredictionInput(BaseModel):
    ad_spend: float
    temperature: float
    day_of_week: str # e.g., "Sunday", "Monday"

class PredictionOutput(BaseModel):
    predicted_sales: float

# --- API Endpoints ---
@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionOutput, tags=["Prediction"])
def predict(input_data: PredictionInput):
    """Predicts sales based on input data."""
    if model_payload is None:
        raise HTTPException(status_code=503, detail="Model not trained. Please call the /train endpoint first.")

    model = model_payload['model']
    model_columns = model_payload['columns']

    # Create a DataFrame from the input
    input_df = pd.DataFrame([input_data.dict()])

    # One-hot encode the day_of_week
    input_df_encoded = pd.get_dummies(input_df)

    # Align columns with the training data. This is crucial.
    final_df = input_df_encoded.reindex(columns=model_columns, fill_value=0)

    # Make prediction
    try:
        prediction = model.predict(final_df)[0]
        return PredictionOutput(predicted_sales=prediction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/train", tags=["Training"])
def train_endpoint():
    """Retrains the model and reloads it in the application."""
    try:
        # Run the training function
        train_model()
        # Reload the model in the current app instance
        load_model()
        return {"message": "Model training successful. The new model is now active."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

import fastapi

import pandas as pd
from pydantic import BaseModel
from typing import List
import joblib

from challenge.model import DelayModel
from challenge.request_model import PredictRequest

app = fastapi.FastAPI()

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(request: PredictRequest) -> dict:
    model = DelayModel()
    
    data = pd.DataFrame([f.dict() for f in request.flights])
    preprocessed_data = model.preprocess(data, target_column=None)

    predictions = model.predict(preprocessed_data)
    return {"predict": predictions}

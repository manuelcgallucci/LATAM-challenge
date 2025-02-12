# -*- coding: utf-8 -*-
from pydantic import BaseModel, validator
from fastapi import HTTPException, status
from typing import List


class FlightData(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int

    @validator("OPERA")
    def validate_opera(cls, value):
        ALLOWED_OPERA = [
            "Grupo LATAM",
            "Sky Airline",
            "Aerolineas Argentinas",
            "Copa Air",
            "Latin American Wings",
            "Avianca",
            "JetSmart SPA",
            "Gol Trans",
            "American Airlines",
            "Air Canada",
            "Iberia",
            "Delta Air",
            "Air France",
            "Aeromexico",
            "United Airlines",
            "Oceanair Linhas Aereas",
            "Alitalia",
            "K.L.M.",
            "British Airways",
            "Qantas Airways",
            "Lacsa",
            "Austral",
            "Plus Ultra Lineas Aereas",
        ]
        if value not in ALLOWED_OPERA:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"OPERA value unkown: {value}")
        return value

    @validator("TIPOVUELO")
    def validate_tipovuelo(cls, value):
        ALLOWED_TIPOVUELO = ["N", "I"]
        if value not in ALLOWED_TIPOVUELO:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"TIPOVUELO must be one of: {', '.join(ALLOWED_TIPOVUELO)}. Got {value}",
            )
        return value

    @validator("MES")
    def validate_mes(cls, value):
        if value < 1 or value > 12:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="MES must be between 1 and 12")
        return value


class PredictRequest(BaseModel):
    flights: List[FlightData]

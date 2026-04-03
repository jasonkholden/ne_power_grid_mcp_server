from typing import List
from pydantic import BaseModel, Field
from datetime import datetime


class HourlyLoadForecastEntry(BaseModel):
    """Individual hourly load forecast entry."""
    begin_date: datetime = Field(alias="BeginDate")
    creation_date: datetime = Field(alias="CreationDate")
    load_mw: float = Field(alias="LoadMw")
    net_load_mw: float = Field(alias="NetLoadMw")

    class Config:
        populate_by_name = True


class HourlyLoadForecastsWrapper(BaseModel):
    """Inner wrapper containing the list of forecast entries."""
    hourly_load_forecast: List[HourlyLoadForecastEntry] = Field(alias="HourlyLoadForecast")

    class Config:
        populate_by_name = True


class HourlyLoadForecastResponse(BaseModel):
    """Complete hourly load forecast API response."""
    hourly_load_forecasts: HourlyLoadForecastsWrapper = Field(alias="HourlyLoadForecasts")

    class Config:
        populate_by_name = True

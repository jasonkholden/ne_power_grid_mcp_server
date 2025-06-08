from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class FuelMixEntry(BaseModel):
    """Individual fuel mix entry."""
    begin_date: datetime = Field(alias="BeginDate")
    gen_mw: float = Field(alias="GenMw")
    fuel_category_rollup: str = Field(alias="FuelCategoryRollup")
    fuel_category: str = Field(alias="FuelCategory")
    marginal_flag: str = Field(alias="MarginalFlag")
    
    class Config:
        populate_by_name = True

class GenFuelMixData(BaseModel):
    """Container for the fuel mix array."""
    gen_fuel_mix: List[FuelMixEntry] = Field(alias="GenFuelMix")
    
    class Config:
        populate_by_name = True
    
class FuelMixResponse(BaseModel):
    """Complete fuel mix API response."""
    gen_fuel_mixes: GenFuelMixData = Field(alias="GenFuelMixes")
    
    class Config:
        populate_by_name = True

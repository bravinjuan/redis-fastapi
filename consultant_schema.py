# IMPORTS -------------------------------------------------------------
from pydantic import BaseModel
from typing import Optional, Union
from sqlalchemy import schema
from datetime import datetime
from typing import List, Union
# IMPORTS -------------------------------------------------------------


# Clase para controlar el tipo de dato recibido al crear un nuevo consultant
class Consultant_create(BaseModel):
    name: str
    lastName: str
    legajo: str
    startDate: Optional[datetime]
    endDate: Union[datetime, None]
    seniority: str
    billable: Union[bool, str]
    availability: float
    englishLevel: int


# Clase para devolver datos de consultant
class Consultant_info(BaseModel):
    id: str
    name: str
    lastName: Optional[str]
    legajo: str
    startDate: Optional[datetime]
    endDate: Optional[datetime]
    seniority: str
    availability: float
    billable: Optional[bool]
    englishLevel: int
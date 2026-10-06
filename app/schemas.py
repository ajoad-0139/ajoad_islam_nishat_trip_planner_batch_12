from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


class StrictSchema(BaseModel):
    model_config = ConfigDict(strict=True, str_strip_whitespace=True)


class TripCreate(StrictSchema):
    destination: str = Field(min_length=1, max_length=200)
    start_date: date
    end_date: date
    budget: Decimal = Field(gt=0, max_digits=12, decimal_places=2)   
    max_travelers: int = Field(gt=0)                                 

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date <= self.start_date:                         
            raise ValueError("end_date must be later than start_date")
        return self


TripUpdate = TripCreate


class TravelerCreate(StrictSchema):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr

    @field_validator("email")
    @classmethod
    def lowercase_email(cls, value):
        return value.lower()                                         


class ExpenseCreate(StrictSchema):
    title: str = Field(min_length=1, max_length=200)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)   


class StatusUpdate(StrictSchema):
    status: Literal["PLANNED", "ONGOING", "COMPLETED", "CANCELLED"]
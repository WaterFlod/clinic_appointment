from pydantic import BaseModel, Field

import datetime


class Appointment(BaseModel):
    doctor_id: int = Field(...)
    start_time: datetime.time = Field(...)
    
class AppointmentDTO(Appointment):
    id: int = Field(...)

    
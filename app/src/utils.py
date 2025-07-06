from sqlalchemy import select
from models import AppointmentModel

from schemas import AppointmentDTO

import datetime


async def get_appointments(session) -> list: #return all appointments in DB
    result = await session.execute(select(AppointmentModel))
    appointments = result.scalars().all()
    result_dto = [AppointmentDTO.model_validate(row, from_attributes=True) for row in appointments]
    return result_dto

async def time_to_timedelta(time) -> datetime.timedelta: # converts the type from datetime.time to datetime.timedelta
    time = str(time) # from datetime.time to str
    time = int(time[0:2])*60**2 + int(time[3:5])*60 + int(time[6:8]) # convert everything into seconds
    time = datetime.timedelta(seconds=time) # convert to timedelta
    return time 
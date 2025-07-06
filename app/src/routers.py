from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session

from utils import get_appointments, time_to_timedelta

from schemas import Appointment
from models import AppointmentModel

import datetime


router = APIRouter()


SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("/appointments/{id}", summary="Получить запись по ID.")
async def get_appointment(session:SessionDep, id:int):
    appointments = await get_appointments(session)
    for appointment in appointments:
        if appointment.id == id:
            return appointment
    raise HTTPException(status_code=404, detail="Appointment not found")

@router.post("/appointments", summary="Создать новую запись.")
async def post_appointment(session:SessionDep, data:Appointment):
    appointments = await get_appointments(session) # return all appointments
    flag = True 
    for appointment in appointments:
        appointment_start_time = await time_to_timedelta(appointment.start_time) 
        data_start_time = await time_to_timedelta(data.start_time)
        # The transition is necessary because the datetime.time type cannot be used
        if (appointment.doctor_id == data.doctor_id and 
            abs(appointment_start_time - data_start_time) < datetime.timedelta(minutes=15)): 
            flag = False
    if flag:
        new_appointment = AppointmentModel(
            doctor_id = data.doctor_id,
            start_time = data.start_time
        )
        session.add(new_appointment)
        await session.commit()  
        return {"access": "True", "detail": "Пользователь успешно создан"}
    raise HTTPException(status_code=400, detail="The doctor has an appointment at this time")
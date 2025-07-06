from database import Base

from sqlalchemy.orm import Mapped, mapped_column

from typing import Annotated

import datetime

intpk = Annotated[int, mapped_column(primary_key=True)]

class AppointmentModel(Base):
    __tablename__ = "appointments"
    
    id: Mapped[intpk]
    doctor_id: Mapped[int]
    start_time: Mapped[datetime.time]
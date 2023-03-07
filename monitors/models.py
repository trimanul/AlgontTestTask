import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime

class Base(DeclarativeBase):
    pass

#TODO: better construcotr type hinitng?
class CPULoad(Base):
    """
    CPU load db model
    """
    __tablename__ = "cpu_load"

    id : Mapped[int] = mapped_column(primary_key=True)
    monitor_datetime : Mapped[datetime.datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now())
    cpu_value : Mapped[float] = mapped_column(sa.Float())

    def __repr__(self) -> str:
        return f"CPULoad(id={self.id}, monitor_datetime={self.monitor_datetime},cpu_value={self.cpu_value})"

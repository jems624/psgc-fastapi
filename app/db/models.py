from sqlalchemy import String, Sequence, Text, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase): ...

class Location(Base):
    __tablename__ = 'locations'

    code: Mapped[str] = mapped_column(String(20), primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(100))
    geo_level: Mapped[str] = mapped_column(String(10))
    region: Mapped[str] = mapped_column(String(20), nullable=True)
    province: Mapped[str] = mapped_column(String(20), nullable=True)
    city_municipality: Mapped[str] = mapped_column(String(20), nullable=True)
    # barangay: Mapped[str] = mapped_column(String(20), nullable=True)

from sqlalchemy.orm import declarative_base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column

Base = declarative_base()



class UserProfile(Base):
    __tablename__ = "userprofiles"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)


class Players(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    pvp_kd: Mapped[float]
    user_id: Mapped[int] = mapped_column(ForeignKey("userprofiles.id"), nullable=False)
    pvp_kills: Mapped[int]
    pvp_death: Mapped[int]
    pvp_wins: Mapped[int]
    pvp_lost: Mapped[int]


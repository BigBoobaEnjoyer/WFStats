from pydantic import BaseModel


class PlayerInfo(BaseModel):
    name: str
    pvp_kills: int
    pvp_death: int
    pvp_kd: float
    pvp_wins: int
    pvp_lost: int

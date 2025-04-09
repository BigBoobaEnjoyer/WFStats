from pydantic import BaseModel


class PlayerInfo(BaseModel):
    name: str
    pvp_kills: int
    pvp_death: int
    pvp_kd: float
    pvp_wins: int
    pvp_lost: int

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, PlayerInfo):
            return self.name == other.name
        return NotImplemented

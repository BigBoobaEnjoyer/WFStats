from fastapi import APIRouter

from fixtures import players as fixtures_players
from schema.player import Player

router = APIRouter(prefix="/player", tags=["player"])


@router.get("/all", response_model=list[Player])
async def get_players():
    return fixtures_players

@router.get("/highscore")
async def get_highscore():
    highest = -1
    for player in fixtures_players:
        highest = max(highest, player["score"])
    return highest

@router.post('/new')
async def post_player(new_player:Player):
    fixtures_players.append(new_player)

@router.patch('/name')
async def patch_player(id: int, name):
    for player in fixtures_players:
        if id == player["id"]:
            player["name"] = name



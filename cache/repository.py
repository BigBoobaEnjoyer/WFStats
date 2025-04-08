import asyncio
import json
import logging

from redis.asyncio import Redis
from schema import PlayerInfo
from repository.player import PlayerRepository
logger = logging.getLogger(__name__)

class PlayerCacheRepository:

    def __init__(self, cache_session, player_repository):
        self.cache_session = cache_session
        self.player_repository: PlayerRepository = player_repository

    async def get_all_players(self, key: str = "all_players") -> list | None:
        players_json = None
        async for cache in self.cache_session:
            players_json = await cache.get(key)
            logger.info(msg='getting info from redis')
            if not players_json:
                players = await self.player_repository.get_all_players()
                players_info: list[PlayerInfo] = [PlayerInfo(
                    name=player.name,
                    pvp_kills=player.pvp_kills,
                    pvp_death=player.pvp_death,
                    pvp_kd=player.pvp_kd,
                    pvp_wins=player.pvp_wins,
                    pvp_lost=player.pvp_lost
                ) for player in players]
                players_json = json.dumps([player.model_dump() for player in players_info], ensure_ascii=False)
                await cache.set('all_players', players_json, ex=60)
                logger.info(msg='setting info to redis')
        return [PlayerInfo.model_validate(player) for player in json.loads(players_json)]

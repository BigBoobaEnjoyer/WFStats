
import httpx
import logging



from cache.repository import PlayerCacheRepository
from exceptions.player import PlayerNotFoundException
from repository.player import PlayerRepository
from schema.player import PlayerInfo

logger = logging.getLogger(__name__)


class WFApiPlayer:

    def __init__(self, player_repository, player_cache_repository):
        self.client = httpx.AsyncClient(base_url='https://api.warface.ru')
        self.player_repository: PlayerRepository = player_repository
        self.player_cache_repository: PlayerCacheRepository = player_cache_repository

    async def get_player_info_from_api_by_name(self, player_name) ->PlayerInfo:
        response = await self.client.get(url='/user/stat/', params={"name": player_name})
        player = response.json()

        return PlayerInfo(
            name=player['nickname'],
            pvp_kills=player['kills'],
            pvp_death=player['death'],
            pvp_kd=player['pvp'],
            pvp_wins=player['pvp_wins'],
            pvp_lost=player['pvp_lost']
        )

    async def player_progress_check(self, player_name:str) -> PlayerInfo:
        if not await self.player_repository.get_player_by_name(player_name=player_name):
            raise PlayerNotFoundException(PlayerNotFoundException.detail)
        current_stat = await self.get_player_info_from_api_by_name(player_name)
        last_update_stat = await self.player_repository.get_player_by_name(player_name)
        if (current_stat.pvp_death - last_update_stat.pvp_death) != 0:
            kd = round((current_stat.pvp_kills - last_update_stat.pvp_kills)
                          /(current_stat.pvp_death - last_update_stat.pvp_death), 2)
        else:
            kd = 0
        return PlayerInfo(
            name=player_name,
            pvp_kills=current_stat.pvp_kills - last_update_stat.pvp_kills,
            pvp_death=current_stat.pvp_death - last_update_stat.pvp_death,
            pvp_kd= kd,
            pvp_wins= current_stat.pvp_wins - last_update_stat.pvp_wins,
            pvp_lost=current_stat.pvp_lost - last_update_stat.pvp_lost
        )

    async def update_all_players_stat(self):
        all_players = await self.player_repository.get_all_player_names()
        for player_name in all_players:
            new_stat = await self.get_player_info_from_api_by_name(player_name)
            await self.player_repository.update_player_stat(
                player_name=player_name,
                new_stat=new_stat
            )

    async def get_user_stat(self, user_id: int):
        players = await self.player_repository.get_all_players_of_user(user_id)
        user_stat = PlayerInfo(
            name='',
            pvp_kills=0,
            pvp_death=0,
            pvp_kd=0,
            pvp_wins=0,
            pvp_lost=0,
        )
        for player in players:
            user_stat.name += player.name + ' '
            user_stat.pvp_kills += player.pvp_kills
            user_stat.pvp_death += player.pvp_death
            user_stat.pvp_wins += player.pvp_wins
            user_stat.pvp_lost += player.pvp_lost
        if user_stat.pvp_death != 0:
            user_stat.pvp_kd = round(user_stat.pvp_kills / user_stat.pvp_death, 2)
        return user_stat

    async def current_user_stat(self, user_id) -> PlayerInfo:
        player_names = await self.player_repository.get_all_user_player_names(user_id)
        user_stat = PlayerInfo(
            name='',
            pvp_kills=0,
            pvp_death=0,
            pvp_kd=0,
            pvp_wins=0,
            pvp_lost=0,
        )
        for player_name in player_names:
            player = await self.get_player_info_from_api_by_name(player_name)
            user_stat.name += player.name + ' '
            user_stat.pvp_kills += player.pvp_kills
            user_stat.pvp_death += player.pvp_death
            user_stat.pvp_wins += player.pvp_wins
            user_stat.pvp_lost += player.pvp_lost
            if user_stat.pvp_death != 0:
                user_stat.pvp_kd = round(user_stat.pvp_kills / user_stat.pvp_death, 2)
        return user_stat

    async def get_user_progress(self, user_id: int):
        current_stat = await self.current_user_stat(user_id)
        last_update_stat = await self.get_user_stat(user_id)
        user_stat = PlayerInfo(
            name=current_stat.name,
            pvp_kills=current_stat.pvp_kills - last_update_stat.pvp_kills,
            pvp_death=current_stat.pvp_death - last_update_stat.pvp_death,
            pvp_kd=0,
            pvp_wins=current_stat.pvp_wins - last_update_stat.pvp_wins,
            pvp_lost=current_stat.pvp_lost - last_update_stat.pvp_lost,
        )
        if user_stat.pvp_death != 0:
            user_stat.pvp_kd = round(user_stat.pvp_kills / user_stat.pvp_death, 2)
            return user_stat

    async def get_all_players(self):
        players = await self.player_cache_repository.get_all_players()
        return players

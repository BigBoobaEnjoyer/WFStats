
from sqlalchemy import select, delete
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
import logging


from database.models import Players
from schema import PlayerInfo
from exceptions.player import PlayerNotFoundException

logger = logging.getLogger(__name__)


class PlayerRepository:

    def __init__(self, db_session: Session | AsyncSession):
        self.db_session = db_session

    def get_all_players(self) :
        query = select(Players)
        with self.db_session() as session:
            players: list[Players] = session.execute(query).scalars().all()
            print(type(players))
        return players

    async def get_player_by_name(self, player_name: str) -> PlayerInfo | None:
        query = select(Players).where(Players.name == player_name)
        async with self.db_session() as session:
            player = (await session.execute(query)).scalars().first()
        if player:
            return PlayerInfo(
                name=player.name,
                pvp_kills=player.pvp_kills,
                pvp_death=player.pvp_death,
                pvp_kd=player.pvp_kd,
                pvp_wins=player.pvp_wins,
                pvp_lost=player.pvp_lost
            )

    async def delete_player(self, player_name, user_id):
        logger.debug('get player stat: %s', player_name)
        query = select(Players).where(Players.name == player_name and Players.user_id == user_id)
        async with self.db_session() as session:
            player_to_delete = await session.execute(query)
            if player_to_delete :
                query = delete(Players).where(Players.name == player_name)
                await session.execute(query)
                await session.commit()
                return {"message": f"Игрок {player_name} удален"}
            raise PlayerNotFoundException(PlayerNotFoundException.detail)

    async def add_player(self, player:PlayerInfo, user_id: int):
        query = insert(Players).values(
            user_id=user_id,
            name=player.name,
            pvp_kills=player.pvp_kills,
            pvp_death=player.pvp_death,
            pvp_kd=player.pvp_kd,
            pvp_wins=player.pvp_wins,
            pvp_lost=player.pvp_lost
        )
        async with self.db_session() as session:
            await session.execute(query)
            await session.commit()

    async def get_all_player_names(self) -> set[str]:
        query = select(Players.name)
        async with self.db_session() as session:
            player_names = set((await session.execute(query)).scalars().all())
            return player_names

    async def get_all_user_player_names(self, user_id) -> set[str]:
        query = select(Players.name).where(Players.user_id == user_id)
        async with self.db_session() as session:
            player_names = set((await session.execute(query)).scalars().all())
            return player_names

    async def update_player_stat(self, player_name: str, new_stat: PlayerInfo):
        async with self.db_session() as session:
            query = select(Players).where(Players.name == player_name)
            players = (await (session.execute(query))).scalars().all()
            for player in players:
                user_id = player.user_id
                player.user_id = user_id
                player.pvp_kills= new_stat.pvp_kills
                player.pvp_death = new_stat.pvp_death
                player.pvp_kd = new_stat.pvp_kd
                player.pvp_wins = new_stat.pvp_wins
                player.pvp_lost = new_stat.pvp_lost
            await session.commit()

    async def get_all_players_of_user(self, user_id) -> list[Players]:
        query = select(Players).where(Players.user_id == user_id)
        async with self.db_session() as session:
            players = (await session.execute(query)).scalars().all()
            return players

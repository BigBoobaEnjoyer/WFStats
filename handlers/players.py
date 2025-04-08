from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from dependecy import (get_players_repository, get_request_user_id, get_wf_api_players_service,
     get_players_repository_async, get_wf_api_players_service_redis)
from exceptions.player import PlayerNotFoundException
from repository import PlayerRepository
from schema import PlayerInfo
from service.players import  WFApiPlayer


router = APIRouter(prefix="/players", tags=["players"])

@router.post('/new')
async def create_player(
        player_name: str,
        wf_api_player_service: Annotated[WFApiPlayer, Depends(get_wf_api_players_service)],
        player_repository: Annotated[PlayerRepository, Depends(get_players_repository_async)],
        user_id:int = Depends(get_request_user_id)
):
    try:
        player = await wf_api_player_service.get_player_info_from_api_by_name(player_name=player_name)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail='Игрок не найден'
        )
    await player_repository.add_player(player=player, user_id=user_id)
    return player

@router.delete('/delete')
async def delete_player(
        player_name: str,
        player_repository: Annotated[PlayerRepository, Depends(get_players_repository_async)],
        user_id: int = Depends(get_request_user_id),
):
    try:
        player = await player_repository.delete_player(player_name, user_id=user_id)
    except PlayerNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
    return player

@router.get('/search_player', response_model=PlayerInfo)
async def search_player(
        player_name: str,
        wf_player_api_service: Annotated[WFApiPlayer, Depends(get_wf_api_players_service)],
):
    try:
        player = await wf_player_api_service.get_player_info_from_api_by_name(player_name=player_name)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail='Игрок не найден'
        )
    return player

@router.get("/get_all_players")
async def get_all_players(
        wf_player_api_service: Annotated[WFApiPlayer, Depends(get_wf_api_players_service_redis)]
):
    return await wf_player_api_service.get_all_players()

@router.get('/player_progress_check')
async def player_progress_check(
        wf_player_api_service: Annotated[WFApiPlayer, Depends(get_wf_api_players_service)],
        player_name: str
):
    try:
        player_progress = await wf_player_api_service.player_progress_check(player_name)
    except PlayerNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
    return player_progress

@router.get('/all_players_names')
async def get_all_player_names(
        player_repository: Annotated[PlayerRepository, Depends(get_players_repository_async)]
):
    return await player_repository.get_all_player_names()

@router.get('/user_stat')
async def get_user_stat(
        wf_player_api_service: Annotated[WFApiPlayer, Depends(get_wf_api_players_service)],
        user_id: int = Depends(get_request_user_id)
):
    return await wf_player_api_service.get_user_stat(user_id)

@router.get('/get_player_current_stat')
async def get_current_user_stat(
        wf_player_api_service: Annotated[WFApiPlayer, Depends(get_wf_api_players_service)],
        user_id: int = Depends(get_request_user_id)
):
    return await wf_player_api_service.current_user_stat(user_id)

@router.get('/get_user_progress')
async def get_user_progress(
        wf_player_api_service: Annotated[WFApiPlayer, Depends(get_wf_api_players_service)],
        user_id: int = Depends(get_request_user_id)
):
    return await wf_player_api_service.get_user_progress(user_id=user_id)

@router.put("/update_player_stat")
async def update_player_stat(
        player_repository: Annotated[PlayerRepository, Depends(get_players_repository_async)],
        wf_player_api_service: Annotated[WFApiPlayer, Depends(get_wf_api_players_service)],
        player_name: str
):
    new_stat = await wf_player_api_service.get_player_info_from_api_by_name(player_name=player_name)
    await player_repository.update_player_stat(player_name=player_name, new_stat=new_stat)

@router.put('/update_all_players_stat')
async def update_all_players_stat(
        wf_player_api_service: Annotated[WFApiPlayer, Depends(get_wf_api_players_service)]
):
    await wf_player_api_service.update_all_players_stat()


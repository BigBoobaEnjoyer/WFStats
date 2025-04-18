import pytest

from app.handlers.auth import login
from app.modules.user import UserCreateSchema, AuthService


@pytest.mark.asyncio
async def test_login():
    result = await login(
        body=UserCreateSchema(username='string', password='string'),
        auth_service= AuthService
    )
    assert result['user_id'] == 9

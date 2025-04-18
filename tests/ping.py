import pytest


from app.handlers.ping import ping

@pytest.mark.asyncio
async def test_ping():
    assert await ping() == 'pong'

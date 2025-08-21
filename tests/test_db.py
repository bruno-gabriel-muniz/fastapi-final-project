from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest
from freezegun import freeze_time
from sqlalchemy.ext.asyncio import AsyncSession

from src.tcc_madrs.models import User

# from time import sleep


@pytest.mark.asyncio
async def test_created_at(session: AsyncSession):
    with freeze_time(datetime.now(ZoneInfo('UTC'))) as time_test:
        user = User('test', 'test@example.com', 'secret')
        session.add(user)
        await session.commit()
        await session.refresh(user)

    assert abs(user.created_at - time_test.time_to_freeze) <= timedelta(
        seconds=1
    )
    assert abs(user.updated_at - time_test.time_to_freeze) <= timedelta(
        seconds=1
    )


@pytest.mark.asyncio
async def test_updated_at(session: AsyncSession):
    with freeze_time(datetime.now(ZoneInfo('UTC'))) as time_test:
        user = User('test', 'test@example.com', 'secret')
        session.add(user)
        await session.commit()
        await session.refresh(user)

    # sleep(1)

    with freeze_time(datetime.now(ZoneInfo('UTC'))) as time2_test:
        user.username = 'tested'
        session.add(user)
        await session.commit()
        await session.refresh(user)

    assert abs(user.created_at - time_test.time_to_freeze) <= timedelta(
        seconds=1
    )
    assert abs(user.updated_at - time2_test.time_to_freeze) <= timedelta(
        seconds=1
    )

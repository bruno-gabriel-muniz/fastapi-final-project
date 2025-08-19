from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from freezegun import freeze_time

from src.tcc_madrs.models import User

# from time import sleep


def test_created_at(session):
    with freeze_time(datetime.now(ZoneInfo('UTC'))) as time_test:
        user = User('test', 'test@example.com', 'secret')
        session.add(user)
        session.commit()
        session.refresh(user)

    assert abs(user.created_at - time_test.time_to_freeze) <= timedelta(
        seconds=1
    )
    assert abs(user.updated_at - time_test.time_to_freeze) <= timedelta(
        seconds=1
    )


def test_updated_at(session):
    with freeze_time(datetime.now(ZoneInfo('UTC'))) as time_test:
        user = User('test', 'test@example.com', 'secret')
        session.add(user)
        session.commit()
        session.refresh(user)

    # sleep(1)

    with freeze_time(datetime.now(ZoneInfo('UTC'))) as time2_test:
        user.username = 'tested'
        session.add(user)
        session.commit()
        session.refresh(user)

    assert abs(user.created_at - time_test.time_to_freeze) <= timedelta(
        seconds=1
    )
    assert abs(user.updated_at - time2_test.time_to_freeze) <= timedelta(
        seconds=1
    )

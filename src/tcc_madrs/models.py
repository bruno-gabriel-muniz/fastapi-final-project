from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


@table_registry.mapped_as_dataclass
class Novelist:
    __tablename__ = 'novelist'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    name: Mapped[str] = mapped_column(unique=True)

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


# @table_registry.mapped_as_dataclass
# class Book:
#     __tablename__ = 'books'

#     id: Mapped[int] = mapped_column(primary_key=True, init=False)

#     year: Mapped[int]
#     name: Mapped[str] = mapped_column(unique=True)
#     romancista_id: Mapped[int]

#     created_at: Mapped[datetime] = mapped_column(
#         init=False, server_default=func.now()
#     )
#     updated_at: Mapped[datetime] = mapped_column(
#         init=False,
#         server_default=func.now(),
#         onupdate=func.now(),
#     )

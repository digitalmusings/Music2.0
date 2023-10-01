"""
SQLAlchemy ORM - Bracket

A bracket row encompasses a single entire music bracket, including all
submissions, play-ins, regular rounds, and individual matches. Any given bracket
theme (some combination of type + name + year range) may be repeated any number
of times, each a separate row. The main bracket type is the broad year-specific
bracket, which should only exist once per epoch. Side brackets are not
necessarily tied to an epoch.
"""

import datetime

from sqlalchemy import orm

from music2.common.models import base

__all__ = ("Bracket",)


class Bracket(base.Base):
    __tablename__ = "bracket"

    bracket_id: orm.Mapped[base.pk]
    epoch: orm.Mapped[int | None]
    cycle: orm.Mapped[int | None]
    name: orm.Mapped[str | None]
    type: orm.Mapped[str] = orm.mapped_column(comment="year theme aggregate")
    year_min: orm.Mapped[int | None]
    year_max: orm.Mapped[int | None]
    order: orm.Mapped[int]
    size: orm.Mapped[int] = orm.mapped_column(comment="128 96 64 48 32")
    date_start: orm.Mapped[datetime.datetime | None]
    date_end: orm.Mapped[datetime.datetime | None]
    discord_message_id: orm.Mapped[str | None]

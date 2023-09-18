"""
SQLAlchemy ORM - Participant, ParticipantNickname

The participant table stores information about any Discord user participating in
any capacity, whether submitting or simply voting.

The participant_nickname table stores all the known nicknames for a given user.
This is particularly helpful for matching up submissions via HTML forms, e.g.,
with Discord users.
"""

import datetime

import sqlalchemy
from sqlalchemy import orm

from music2.models import base

__all__ = ("Participant", "ParticipantNickname")


class Participant(base.Base):
    __tablename__ = "participant"

    participant_id: orm.Mapped[base.pk]
    username: orm.Mapped[str]
    discriminator: orm.Mapped[int | None]
    nickname: orm.Mapped[str | None] = orm.mapped_column(comment="CALCULATED")
    date_joined: orm.Mapped[datetime.datetime] = orm.mapped_column(
        server_default=sqlalchemy.text("now()")
    )
    time_zone: orm.Mapped[str | None]
    active: orm.Mapped[bool]


class ParticipantNickname(base.Base):
    __tablename__ = "participant_nickname"

    participant_nickname_id: orm.Mapped[base.pk]
    participant_id: orm.Mapped[base.fk]
    nickname: orm.Mapped[str]
    date_start: orm.Mapped[datetime.datetime] = orm.mapped_column(
        server_default=sqlalchemy.text("now()")
    )
    date_end: orm.Mapped[datetime.datetime | None]

    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["participant_id"], ["participant.participant_id"], ondelete="CASCADE"
        ),
    )

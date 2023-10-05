"""
SQLAlchemy ORM - Round

A round represents a single block of votable matches with a bracket. This may be
a standard elimination round or a play-in round before the bracket proper
begins. In general, normal rounds contain a number of matches equal to a power
of two, each pairing two songs up, but play-ins may have any number of matches,
and the final round may contain both a final match and a third place match.
"""

import datetime

import sqlalchemy
from sqlalchemy import orm

from music2.common.models import base

__all__ = ("Round",)


class Round(base.Base):
    __tablename__ = "round"

    round_id: orm.Mapped[base.pk]
    bracket_id: orm.Mapped[base.fk]
    name: orm.Mapped[str] = orm.mapped_column(
        comment=(
            'Finals "Third Place" "Semi-Finals" "Quarter-Finals" "Round of 16" '
            '"Round of 32" "Round of 64" "Round of 128" "Play-Ins"'
        )
    )
    size: orm.Mapped[int] = orm.mapped_column(comment="0 means play-in round")
    index_asc: orm.Mapped[int] = orm.mapped_column(comment="-1-indexed from Play-Ins")
    index_desc: orm.Mapped[int] = orm.mapped_column(comment="0-indexed from Finals")
    date_start: orm.Mapped[base.datetime_now]
    date_end: orm.Mapped[datetime.datetime | None]
    discord_message_id: orm.Mapped[str | None]

    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["bracket_id"], ["bracket.bracket_id"], ondelete="CASCADE"
        ),
    )

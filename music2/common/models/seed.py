"""
SQLAlchemy ORM - Seed, SeedHistory

The seed table represents which submissions were chosen and in what order they
are to be matched in a given bracket.

The seed_history table contains a record of any manual changes made to the
seeding, such as an uncaught dupe or ineligible song being replaced or a user
desiring to replace their submission after the bracket has begun.
"""

import datetime
import uuid

import sqlalchemy
from sqlalchemy import orm

from music2.common.models import base

__all__ = ("Seed", "SeedHistory")


class Seed(base.Base):
    __tablename__ = "seed"

    seed_id: orm.Mapped[base.pk]
    bracket_id: orm.Mapped[base.fk]
    seed: orm.Mapped[int] = orm.mapped_column(index=True)
    submission_id: orm.Mapped[base.fk]
    emoji: orm.Mapped[str]

    __table_args__ = (
        sqlalchemy.UniqueConstraint("bracket_id", "seed"),
        sqlalchemy.ForeignKeyConstraint(
            ["bracket_id"], ["bracket.bracket_id"], ondelete="CASCADE"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["submission_id"], ["submission.submission_id"], ondelete="CASCADE"
        ),
    )


class SeedHistory(base.Base):
    __tablename__ = "seed_history"

    # These are specific to the seed_history log
    seed_history_id: orm.Mapped[base.pk]
    update_date: orm.Mapped[base.datetime_now]
    update_note: orm.Mapped[str] = orm.mapped_column(comment='"missed dupe" ineligible')

    # These just duplicate the data from the seed row
    seed_id: orm.Mapped[base.fk]
    submission_id: orm.Mapped[base.fk]
    emoji: orm.Mapped[str]

    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["seed_id"], ["seed.seed_id"], ondelete="CASCADE"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["submission_id"], ["submission.submission_id"], ondelete="CASCADE"
        ),
    )

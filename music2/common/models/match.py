"""
SQLAlchemy ORM - Match, MatchSeed

A match represents a single matchup of two or more songs within a given round of
voting in a bracket. A match may be cancelled and so removed from the round. Any
match with a non-null `date_cancelled` should be considered cancelled and not
part of the actual bracket. The winner of a given match advances to the next
match, indicated by the `next_match_id`.

A match_seed row represents a single song within a match. It is tied to a
specific user submission via the seed table and keeps track of the number of
votes and who voted for it. If a song in a given match has advanced from a
previous match, this is recorded in `previous_match_id`.
"""

import datetime

import sqlalchemy
from sqlalchemy import orm

from music2.common.models import base

__all__ = ("Match", "MatchSeed")


class Match(base.Base):
    __tablename__ = "match"

    match_id: orm.Mapped[base.pk]
    round_id: orm.Mapped[base.fk]
    index: orm.Mapped[int]
    date_posted: orm.Mapped[datetime.datetime | None]
    tie: orm.Mapped[int] = orm.mapped_column(comment="0 (no), 1 (broken), 2 (kept)")
    winner_id: orm.Mapped[base.fk | None]
    date_cancelled: orm.Mapped[datetime.datetime | None]
    reason_cancelled: orm.Mapped[str | None] = orm.mapped_column(
        comment='"ineligible sub0" "ineligible sub1" "administrative error"'
    )
    next_match_id: orm.Mapped[base.fk | None]
    discord_message_id: orm.Mapped[str | None]

    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["round_id"], ["round.round_id"], ondelete="CASCADE"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["winner_id"], ["submission.submission_id"], ondelete="SET NULL"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["next_match_id"], ["match.match_id"], ondelete="SET NULL"
        ),
    )


class MatchSeed(base.Base):
    __tablename__ = "match_seed"

    match_seed_id: orm.Mapped[base.pk]
    match_id: orm.Mapped[base.fk]
    seed_id: orm.Mapped[base.fk]
    index: orm.Mapped[int]
    votes: orm.Mapped[int]
    voters: orm.Mapped[list[str]]
    previous_match_id: orm.Mapped[base.fk | None]

    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["match_id"], ["match.match_id"], ondelete="CASCADE"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["seed_id"], ["seed.seed_id"], ondelete="CASCADE"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["previous_match_id"], ["match.match_id"], ondelete="SET NULL"
        ),
    )

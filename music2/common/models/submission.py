"""
SQLAlchemy ORM - Submission, SubmissionHistory

The submission table stores an exact record of what a user entered when
submitting a song, as well as a link to the parsed song in the song table.

The submission_history table is a log of any changes made to the submissions,
either by the user via a command or by an admin.
"""

import sqlalchemy
from sqlalchemy import orm

from music2.common.models import base

__all__ = ("Submission", "SubmissionHistory")


class Submission(base.Base):
    __tablename__ = "submission"

    submission_id: orm.Mapped[base.pk]
    participant_id: orm.Mapped[base.fk]
    bracket_id: orm.Mapped[base.fk]
    song_id: orm.Mapped[base.fk]
    order: orm.Mapped[int]
    date_submitted: orm.Mapped[base.datetime_now]
    active: orm.Mapped[bool]
    is_dupe: orm.Mapped[bool]
    title: orm.Mapped[str]
    version: orm.Mapped[str | None]
    artist: orm.Mapped[str | None]
    collaborators: orm.Mapped[str | None]
    composers: orm.Mapped[str | None]
    link: orm.Mapped[str]
    genre: orm.Mapped[str | None]
    emoji: orm.Mapped[str | None]
    comments: orm.Mapped[str | None]

    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["participant_id"], ["participant.participant_id"], ondelete="CASCADE"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["bracket_id"], ["bracket.bracket_id"], ondelete="CASCADE"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["song_id"], ["song.song_id"], ondelete="CASCADE"
        ),
    )


class SubmissionHistory(base.Base):
    __tablename__ = "submission_history"

    # These are specific to the submission_history log
    submission_history_id: orm.Mapped[base.pk]
    update_date: orm.Mapped[base.datetime_now]
    update_note: orm.Mapped[str] = orm.mapped_column(
        comment='dupe ineligible withdrawn "play-in loser"'
    )

    # These just duplicate the data from the submission row
    submission_id: orm.Mapped[base.fk]
    participant_id: orm.Mapped[base.fk]
    bracket_id: orm.Mapped[base.fk]
    song_id: orm.Mapped[base.fk]
    order: orm.Mapped[int]
    date_submitted: orm.Mapped[base.datetime_now]
    active: orm.Mapped[bool]
    is_dupe: orm.Mapped[bool]
    title: orm.Mapped[str]
    version: orm.Mapped[str | None]
    artist: orm.Mapped[str | None]
    collaborators: orm.Mapped[str | None]
    composers: orm.Mapped[str | None]
    link: orm.Mapped[str]
    genre: orm.Mapped[str | None]
    emoji: orm.Mapped[str | None]
    comments: orm.Mapped[str | None]

    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["submission_id"], ["submission.submission_id"], ondelete="CASCADE"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["participant_id"], ["participant.participant_id"], ondelete="CASCADE"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["bracket_id"], ["bracket.bracket_id"], ondelete="CASCADE"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["song_id"], ["song.song_id"], ondelete="CASCADE"
        ),
    )

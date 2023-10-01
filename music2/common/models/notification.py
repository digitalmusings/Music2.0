"""
SQLAlchemy ORM - Notification

A notification represents any attempt on the part of the bot to contact a user,
e.g. if a submission has duped and needs replacement.
"""

import datetime

import sqlalchemy
from sqlalchemy import orm

from music2.common.models import base

__all__ = ("Notification",)


class Notification(base.Base):
    __tablename__ = "notification"

    notification_id: orm.Mapped[base.pk]
    participant_id: orm.Mapped[base.fk]
    submission_id: orm.Mapped[base.fk | None]
    date_first_attempt: orm.Mapped[base.datetime_now]
    date_succeeded: orm.Mapped[datetime.datetime | None]
    notification_type: orm.Mapped[str] = orm.mapped_column(
        comment='"need replacement" "no replacement" "tie"'
    )
    discord_message_id: orm.Mapped[str | None]

    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["participant_id"], ["participant.participant_id"], ondelete="CASCADE"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["submission_id"], ["submission.submission_id"], ondelete="SET NULL"
        ),
    )

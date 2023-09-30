"""
SQLAlchemy ORM - Project, Config, BracketSelection

Each deployed instance of the entire project should have a distinct row (and
corresponding set of rows in the config table) in the project table. These
projects can be run concurrently and share the same backing database and
historic data without interfering with each other.

The config table is for storing project-specific key-value pairs, such as
Discord server ID or project metadata.

A row in the bracket_selection table corresponds to the decision to run a
specific bracket, made on a given date and for a given epoch+cycle. It requires
that the bracket row itself be created before the bracket_selection row.
"""

import uuid

import sqlalchemy
from sqlalchemy import orm

from music2.models import base

__all__ = ("BracketSelection", "Config", "Project")


class Project(base.Base):
    __tablename__ = "project"

    project_id: orm.Mapped[base.pk]
    name: orm.Mapped[str] = orm.mapped_column(unique=True)
    project_lead_id: orm.Mapped[uuid.UUID | None]

    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["project_lead_id"], ["participant.participant_id"], ondelete="SET NULL"
        ),
    )


class Config(base.Base):
    __tablename__ = "config"

    project_id: orm.Mapped[uuid.UUID]
    key: orm.Mapped[str]
    value: orm.Mapped[str | None]

    __table_args__ = (
        sqlalchemy.PrimaryKeyConstraint("project_id", "key"),
        sqlalchemy.ForeignKeyConstraint(
            ["project_id"], ["project.project_id"], ondelete="CASCADE"
        ),
    )


class BracketSelection(base.Base):
    __tablename__ = "bracket_selection"

    bracket_selection_id: orm.Mapped[base.pk]
    project_id: orm.Mapped[base.fk]
    epoch: orm.Mapped[int]
    cycle: orm.Mapped[int]
    bracket_id: orm.Mapped[base.fk]
    date_selected: orm.Mapped[base.datetime_now]

    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["project_id"], ["project.project_id"], ondelete="CASCADE"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["bracket_id"], ["bracket.bracket_id"], ondelete="CASCADE"
        ),
    )

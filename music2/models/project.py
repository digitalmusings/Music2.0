"""
SQLAlchemy ORM - Project, Config

Each deployed instance of the entire project should have a distinct row (and
corresponding set of rows in the config table) in the project table. These
projects can be run concurrently and share the same backing database and
historic data without interfering with each other.

The config table is for storing project-specific key-value pairs, such as
Discord server ID or project metadata.
"""

import uuid

import sqlalchemy
from sqlalchemy import orm

from music2.models import base

__all__ = ("Config", "Project")


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

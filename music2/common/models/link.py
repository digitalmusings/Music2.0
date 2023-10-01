"""
SQLAlchemy ORM - Link, LinkRelation

Each row of the link table represents a URL to listen to a (possibly region-
specific) performance/version of a song.

The link_relation table connects alternate URLs to their parent submission,
song, or bracket entry.
"""

import sqlalchemy
from sqlalchemy import orm

from music2.common.models import base

__all__ = ("Link", "LinkRelation")


class Link(base.Base):
    __tablename__ = "link"

    link_id: orm.Mapped[base.pk]
    url: orm.Mapped[str]
    region: orm.Mapped[list[str] | None] = orm.mapped_column(
        comment=(
            'US Canada Japan Australia Europe Asia "North America" "South America"'
            " Africa Worldwide"
        )
    )


class LinkRelation(base.Base):
    __tablename__ = "link_relation"

    link_relation_id: orm.Mapped[base.pk]
    parent_link_id: orm.Mapped[base.fk]
    child_link_id: orm.Mapped[base.fk]
    link_relation_type: orm.Mapped[str] = orm.mapped_column(
        comment="submission song seed"
    )

    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["parent_link_id"], ["link.link_id"], ondelete="CASCADE"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["child_link_id"], ["link.link_id"], ondelete="CASCADE"
        ),
    )

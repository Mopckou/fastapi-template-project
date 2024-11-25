import datetime
from typing import List, Optional

from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.utils.database import Base


DEPTH = 5


class SpaceModel(Base):
    __tablename__ = "spaces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.datetime.now)
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey("spaces.id"))

    parent: Mapped[Optional['SpaceModel']] = relationship(remote_side=[id], lazy="joined", join_depth=DEPTH)

    def __repr__(self):
        return f"<SpaceModel(id={self.id}, " \
               f"name=\"{self.name}\", " \
               f"parent_id=\"{self.parent_id}\", " \
               f"created_at=\"{self.created_at}\", " \
               f"updated_at=\"{self.updated_at}\">"

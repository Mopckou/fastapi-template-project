import datetime
import uuid
from typing import List

from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.utils.database import Base


class ProjectModel(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.datetime.now)

    spaces_associations: Mapped[List['ProjectSpaceModel']] = relationship(back_populates="project")
    space: Mapped["SpaceModel"] = relationship( # noqa
        secondary="projects_spaces", back_populates="projects", viewonly=True
    )

    def __repr__(self):
        return f"<ProjectModel(id={self.id}, " \
               f"name=\"{self.name}\", " \
               f"created_at=\"{self.created_at}\", " \
               f"updated_at=\"{self.updated_at}\">"


class ProjectSpaceModel(Base):
    __tablename__ = "projects_spaces"

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), primary_key=True)
    space_id: Mapped[str] = mapped_column(ForeignKey("spaces.id"), primary_key=True)

    project: Mapped["ProjectModel"] = relationship(back_populates="spaces_associations")
    space: Mapped["SpaceModel"] = relationship(back_populates="projects_associations") # noqa

    def __repr__(self):
        return f"<ProjectSpaceModel(project_id={self.project_id}, " \
               f"space_id=\"{self.space_id}\">"


import datetime
import uuid

from sqlalchemy import Column, String, Integer, DateTime, Uuid, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.utils.database import Base


class UserModel(Base):

    __tablename__ = "users"

    id: Mapped[Uuid] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    middle_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, onupdate=datetime.datetime.now)

    password: Mapped["PasswordModel"] = relationship(back_populates="user", lazy="selectin")

    def __repr__(self):
        return f"<UserModel(id={self.id}, " \
               f"email=\"{self.email}\", " \
               f"first_name=\"{self.first_name}\", " \
               f"middle_name=\"{self.middle_name}\", " \
               f"last_name=\"{self.last_name}\">"


class PasswordModel(Base):

    __tablename__ = "passwords"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"))
    hash: Mapped[str] = mapped_column(String, nullable=False)
    salt: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, onupdate=datetime.datetime.now)

    user: Mapped[UserModel] = relationship(back_populates="password")

    def __repr__(self):
        return f"<Password(id={self.id}, " \
               f"user_id=\"{self.user_id}\", " \
               f"hash=\"{self.hash}\", " \
               f"created_at=\"{self.created_at}\", " \
               f"updated_at=\"{self.updated_at}\">"

from sqlalchemy import Column, String, Integer

from app.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, " \
               f"email=\"{self.email}\", " \
               f"first_name=\"{self.first_name}\", " \
               f"middle_name=\"{self.middle_name}\", " \
               f"last_name=\"{self.last_name}\">"

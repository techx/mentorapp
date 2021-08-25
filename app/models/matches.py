from app import db
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    Text,
    String,
)

class Matches(db.Model):

    __tablename__ = "matches"

    team_id = Column(Integer, primary_key=True, nullable=False)
    mentor_id = Column(Integer)

    def populate(self, team_id, mentor_id):
        self.team_id = team_id
        self.mentor_id = mentor_id

    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return data

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    
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

    @classmethod
    def populate(self, data):
        for key, val in data.items():
            row = db.session.query(Matches).filter_by(team_id=key).first()
            if not row:
                row = Matches()
                row.team_id= key
                row.mentor_id= val
                db.session.add(row)
            else:
                row.mentor_id = val
        db.session.commit()

    @classmethod
    def delete(self, data):
        for key in data:
            db.session.query(Matches).filter_by(team_id=key).delete()
        db.session.commit()

    @classmethod
    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return data

    @classmethod
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    
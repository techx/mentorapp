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
    team_email = Column(String)
    mentor_email = Column(String)

    @classmethod
    def populate(self, data):
        for key, val in data.items():
            row = db.session.query(Matches).filter_by(team_id=key).first()
            if not row:
                row = Matches()
                row.team_id= key
                row.mentor_id= val[0]
                row.team_email = val[1]
                row.mentor_email = val[2]
                db.session.add(row)
            else:
                row.mentor_id = val[0]
                row.team_email = val[1]
                row.mentor_email = val[2]
        db.session.commit()

    @classmethod
    def delete(self, data):
        for key in data:
            db.session.query(Matches).filter_by(team_id=key).delete()
        db.session.commit()

    @classmethod
    def deleteAll(self):
        db.session.query(Matches).delete()
        db.session.commit()

    @classmethod
    def serialize(self):
        matches = db.session.query(Matches).all()
        data = {c.team_id: [c.team_email, c.mentor_id, c.mentor_email] for c in matches}
        return data

    @classmethod
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    
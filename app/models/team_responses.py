from app import db
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    Text,
    String,
)

class TeamResponses(db.Model):

    __tablename__ = "team_responses"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text)
    members = Column(Text)
    email = Column(Text)
    commitment = Column(Integer)
    interest = Column(Text)
    virtual = Column(Boolean)

    @classmethod
    def populate(self, name, members, email, commitment, interest, virtual):
        row = db.session.query(TeamResponses).filter_by(name=name).first()
        if not row:
            row = TeamResponses()
            row.name = name
            row.members = members
            row.email = email
            row.commitment = commitment
            row.interest = interest
            row.virtual = virtual
            db.session.add(row)
        else:
            row.members = members
            row.email = email
            row.commitment = commitment
            row.interest = interest
            row.virtual = virtual
        db.session.commit()

    @classmethod
    def serialize(self):
        all = db.session.query(TeamResponses).all()
        data = {c.id: {'commitment': c.commitment, 'interest': set(c.interest.split(',')), 'virtual': c.virtual} for c in all}
        return data

    @classmethod
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
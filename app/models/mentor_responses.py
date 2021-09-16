from app import db
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    Text,
    String,
)

class MentorResponses(db.Model):

    __tablename__ = "mentor_responses"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text)
    email = Column(Text)
    commitment = Column(Integer)
    interest = Column(Text)
    virtual = Column(Boolean)

    @classmethod
    def populate(self, name, email, commitment, interest, virtual):
        row = db.session.query(MentorResponses).filter_by(name=name, email=email, commitment=commitment, interest=interest, virtual=virtual).first()
        if not row:
            row = MentorResponses()
            row.name = name
            row.email = email
            row.commitment = commitment
            row.interest = interest
            row.virtual = virtual
            db.session.add(row)
        else:
            row.email = email
            row.commitment = commitment
            row.interest = interest
            row.virtual = virtual
        db.session.commit()

    @classmethod
    def serialize(self):
        all = db.session.query(MentorResponses).all()
        data = {c.id: {'commitment': c.commitment, 'interest': set(c.interest.split(', ')), 'virtual': c.virtual} for c in all}
        return data

    @classmethod
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def deleteAll(self):
        db.session.query(MentorResponses).delete()
        db.session.commit()
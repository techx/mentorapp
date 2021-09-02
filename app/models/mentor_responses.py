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
    members = Column(ARRAY(Text))
    email = Column(Text)
    commitment = Column(Integer)
    interest = Column(Text)
    virtual = Column(Text)

    def populate(self, name, members, email, commitment, interest, virtual):
        self.name = name
        self.members = members
        self.email = email
        self.commitment = commitment
        self.interest = interest
        self.virtual = virtual

    def serialize(self):
        data = {c.id: {'commitment': c.commitment, 'interest': c.interest, 'virtual': c.virtual} for c in self.__table__.columns}
        return data

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
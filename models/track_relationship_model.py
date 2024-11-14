from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from db.base import Base

class TrackRelationship(Base):
    __tablename__ = 'track_relationship'
    
    track_relationship_id = Column(Integer, primary_key=True)

    # track_id1 = Column(Integer, ForeignKey('track.track_id'), primary_key=True)
    # track_id2 = Column(Integer, ForeignKey('track.track_id'), primary_key=True)
    
    track_id1 = Column(Integer, ForeignKey('track.track_id'))
    track_id2 = Column(Integer, ForeignKey('track.track_id'))

    track1 = relationship('Track', foreign_keys=[track_id1], back_populates='related_tracks')
    track2 = relationship('Track', foreign_keys=[track_id2], back_populates='related_to_tracks')

    __table_args__ = (UniqueConstraint('track_id1', 'track_id2', name='_track_relationship_uc'),)
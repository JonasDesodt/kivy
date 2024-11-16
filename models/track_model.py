from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base

class Track(Base):
    __tablename__ = 'track'
    
    track_id = Column(Integer, primary_key=True)
    artist = Column(String, nullable=False)
    title = Column(String, nullable=False)
    record = Column(String, nullable=True)

    related_tracks = relationship(
        'TrackRelationship',
        foreign_keys='TrackRelationship.track_id1',
        back_populates='track1',
        cascade="all, delete-orphan"
    )
    
    related_to_tracks = relationship(
        'TrackRelationship',
        foreign_keys='TrackRelationship.track_id2',
        back_populates='track2',
        cascade="all, delete-orphan"
    )

    playlist_entries = relationship(
        'PlaylistEntry',
        back_populates='track',
        cascade="all, delete-orphan"
    )
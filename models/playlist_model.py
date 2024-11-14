from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base

class Playlist(Base):
    __tablename__ = 'playlist'

    playlist_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Relationship to PlaylistEntry
    playlist_entries = relationship('PlaylistEntry', back_populates='playlist')
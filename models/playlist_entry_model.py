from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class PlaylistEntry(Base):
    __tablename__ = 'playlist_entry'

    playlist_entry_id = Column(Integer, primary_key=True)

    track_id = Column(Integer, ForeignKey('track.track_id'), nullable=False)
    playlist_id = Column(Integer, ForeignKey('playlist.playlist_id'), nullable=False)

    # Relationships to Track and Playlist
    track = relationship('Track', back_populates='playlist_entries')
    playlist = relationship('Playlist', back_populates='playlist_entries')
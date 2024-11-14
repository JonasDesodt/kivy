from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

class Track(Base):
    __tablename__ = 'track'
    
    track_id = Column(Integer, primary_key=True)
    artist = Column(String, nullable=False)
    title = Column(String, nullable=False)
    record = Column(String, nullable=True)
    
    # Relationships to TrackRelationship and PlaylistEntry
    related_tracks = relationship(
        'TrackRelationship',
        foreign_keys='TrackRelationship.track_id1',
        back_populates='track1'
    )
    
    related_to_tracks = relationship(
        'TrackRelationship',
        foreign_keys='TrackRelationship.track_id2',
        back_populates='track2'
    )

    playlist_entries = relationship('PlaylistEntry', back_populates='track')


class TrackRelationship(Base):
    __tablename__ = 'track_relationship'
    
    track_id1 = Column(Integer, ForeignKey('track.track_id'), primary_key=True)
    track_id2 = Column(Integer, ForeignKey('track.track_id'), primary_key=True)
    
    track1 = relationship('Track', foreign_keys=[track_id1], back_populates='related_tracks')
    track2 = relationship('Track', foreign_keys=[track_id2], back_populates='related_to_tracks')

    __table_args__ = (UniqueConstraint('track_id1', 'track_id2', name='_track_relationship_uc'),)


class Playlist(Base):
    __tablename__ = 'playlist'

    playlist_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Relationship to PlaylistEntry
    playlist_entries = relationship('PlaylistEntry', back_populates='playlist')


class PlaylistEntry(Base):
    __tablename__ = 'playlist_entry'

    playlist_entry_id = Column(Integer, primary_key=True)

    track_id = Column(Integer, ForeignKey('track.track_id'), nullable=False)
    playlist_id = Column(Integer, ForeignKey('playlist.playlist_id'), nullable=False)

    # Relationships to Track and Playlist
    track = relationship('Track', back_populates='playlist_entries')
    playlist = relationship('Playlist', back_populates='playlist_entries')


# Function to create the database and seed it with data
def create_and_seed_database():
    engine = create_engine('sqlite:///playlist.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Sample tracks
    childSupport = Track(artist="Child Abuse & Eric Paul", title="Child Support", record="Imaginary Enemy")
    gooseSteppin = Track(artist="The Flying Luttenbachers", title="Goosesteppin'", record="Shattered Dimension")
    noRemark = Track(artist="DUDS", title="No Remark", record="Of A Nature Or Degree")
    deathSoundBlues = Track(artist="Country Joe & The Fish", title="Death Sound Blues", record="Electric Music For The Mind And Body")    
    wildHorses = Track(artist="MoE", title="Wild Horses", record="Examination Of The Eye Of A Horse")
    
    # Add sample tracks to the session
    session.add_all([childSupport, gooseSteppin, noRemark, deathSoundBlues, wildHorses])
    session.commit()

    # Sample playlist
    playlist1 = Playlist(name="Alternative")
    playlist2 = Playlist(name="Pop")
    
    # Add playlists to the session
    session.add_all([playlist1, playlist2])
    session.commit()

    # Add playlist entries linking tracks to playlists
    entry1 = PlaylistEntry(track_id=childSupport.track_id, playlist_id=playlist1.playlist_id)
    entry2 = PlaylistEntry(track_id=gooseSteppin.track_id, playlist_id=playlist1.playlist_id)
    entry3 = PlaylistEntry(track_id=noRemark.track_id, playlist_id=playlist2.playlist_id)
    entry4 = PlaylistEntry(track_id=deathSoundBlues.track_id, playlist_id=playlist2.playlist_id)
    entry5 = PlaylistEntry(track_id=wildHorses.track_id, playlist_id=playlist1.playlist_id)

    # Add entries to session and commit
    session.add_all([entry1, entry2, entry3, entry4, entry5])
    session.commit()

    # Close session after operations
    session.close()
    engine.dispose()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.playlist_entry_model import PlaylistEntry
from models.playlist_model import Playlist
from models.track_model import Track
from models.track_relationship_model import TrackRelationship
from db.base import Base

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

    session.flush()

    relationship1 = TrackRelationship(track_id1=noRemark.track_id, track_id2=deathSoundBlues.track_id)

    session.add_all([relationship1])
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
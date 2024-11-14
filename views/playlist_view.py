from kivy.uix.recycleview import RecycleView
from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import sessionmaker, joinedload
from app_container import AppContainer
from models.playlist_entry_model import PlaylistEntry

class PlaylistView(RecycleView):
    @inject
    def __init__(self, session_factory: sessionmaker = Provide[AppContainer.session_factory], **kwargs):
        super(PlaylistView, self).__init__(**kwargs)

        self.session = session_factory()

        self.update_data()

    def update_data(self):
        playlistEntries = (
            self.session.query(PlaylistEntry)
            .filter(PlaylistEntry.playlist_id == 1)
            .options(joinedload(PlaylistEntry.track))
            .all()
        )

        self.data = [{
            'playlist_entry_id': playlistEntry.playlist_entry_id,
            'track_id': playlistEntry.track.track_id,
            'artist': playlistEntry.track.artist,
            'title': playlistEntry.track.title,
            'record': playlistEntry.track.record,
            'update_callback': self.update_data  
        } for playlistEntry in playlistEntries]

    def refresh_recycleview(self):
        self.update_data()
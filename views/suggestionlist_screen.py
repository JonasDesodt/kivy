from kivy.uix.screenmanager import Screen
from dependency_injector.wiring import inject, Provide
from app_container import AppContainer
from models.track_relationship_model import TrackRelationship
from sqlalchemy.orm import sessionmaker, joinedload

class SuggestionlistScreen(Screen):
    @inject
    def __init__(self, session_factory: sessionmaker = Provide[AppContainer.session_factory], **kwargs):
        super(SuggestionlistScreen, self).__init__(**kwargs)

        self.session = session_factory()
        
        self.id = 0

        self.data = [
            # {"artist": "Artist 1", "title": "Title 1", "record": "Record 1"},
            # {"artist": "Artist 2", "title": "Title 2", "record": "Record 2"},
            # {"artist": "Artist 3", "title": "Title 3", "record": "Record 3"},
        ]

    def fetch(self):
        suggestions = (
            self.session.query(TrackRelationship)
            .filter(TrackRelationship.track_id1 == self.id)
            .options(joinedload(TrackRelationship.track2))
            .all()
        )

        self.data = [{'artist': tr.track2.artist, 'title': tr.track2.title, 'record': tr.track2.record} for tr in suggestions]
      
        # Now `suggestions` is a list of TrackRelationship objects, not dictionaries
        # self.data = [{'artist': tr.track2.artist, 'title': tr.track2.title, 'record': tr.track2.record} for tr in suggestions]
        # self.ids.suggestionlist_view.data = self.data

    #  def update_data(self):
    #     playlistEntries = (
    #         self.session.query(PlaylistEntry)
    #         .filter(PlaylistEntry.playlist_id == 1)
    #         .options(joinedload(PlaylistEntry.track))
    #         .all()
    #     )

    #     self.data = [{
    #         'playlist_entry_id': playlistEntry.playlist_entry_id,
    #         'track_id': playlistEntry.track.track_id,
    #         'artist': playlistEntry.track.artist,
    #         'title': playlistEntry.track.title,
    #         'record': playlistEntry.track.record,
    #         'update_callback': self.update_data  
    #     } for playlistEntry in playlistEntries]
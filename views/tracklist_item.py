from kivy.uix.boxlayout import BoxLayout
from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import sessionmaker
from app_container import AppContainer
from create_database import PlaylistEntry

class TracklistItem(BoxLayout):   
    @inject
    def __init__(self, session_factory: sessionmaker = Provide[AppContainer.session_factory], **kwargs):
        super().__init__(**kwargs)
        self.track_id = kwargs.get('track_id', None)

        self.session = session_factory()
    
    def add_to_playlist(self, instance):
        if self.track_id is not None:
            new_playlist_entry = PlaylistEntry(track_id=self.track_id, playlist_id=1)
            self.session.add(new_playlist_entry)
            self.session.commit()
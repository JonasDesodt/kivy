from kivy.uix.boxlayout import BoxLayout
from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import sessionmaker
from app_container import AppContainer
from models.playlist_entry_model import PlaylistEntry
from models.track_model import Track

class TracklistItem(BoxLayout):   
    @inject
    def __init__(self, update_callback = None, session_factory: sessionmaker = Provide[AppContainer.session_factory], **kwargs):
        super().__init__(**kwargs)
        self.track_id = kwargs.get('track_id', None)

        self.session = session_factory()

        self.update_callback = update_callback
    
    def add_to_playlist(self, instance):
        if self.track_id is not None:
            new_playlist_entry = PlaylistEntry(track_id=self.track_id, playlist_id=1)
            self.session.add(new_playlist_entry)
            self.session.commit()
    
    def delete_track(self, id):
        track = self.session.query(Track).filter(Track.track_id == id).first()

        if track:          
            self.session.delete(track)
            self.session.commit()

            if self.update_callback:
                self.update_callback()
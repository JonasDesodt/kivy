from kivy.uix.boxlayout import BoxLayout
from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import sessionmaker
from app_container import AppContainer
from models.playlist_entry_model import PlaylistEntry

class PlaylistItem(BoxLayout):
    @inject
    def __init__(self, update_callback = None, session_factory: sessionmaker = Provide[AppContainer.session_factory], **kwargs):
        super().__init__(**kwargs)
        
        self.session = session_factory()

        self.playlist_entry_id = kwargs.get('playlist_entry_id', None)
        self.update_callback = update_callback  # Store the reference to the update callback

    def remove_from_playlist(self, instance):
        if self.playlist_entry_id is not None:
            playlistEntry = self.session.query(PlaylistEntry).filter(PlaylistEntry.playlist_entry_id == self.playlist_entry_id).first()

            if playlistEntry:
                self.session.delete(playlistEntry)
                self.session.commit()

                if self.update_callback:
                    self.update_callback()
from kivy.uix.boxlayout import BoxLayout
from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import sessionmaker
from app_container import AppContainer
from models.track_model import Track

class CreateTrackView(BoxLayout):
    @inject
    def __init__(self, session_factory: sessionmaker = Provide[AppContainer.session_factory], **kwargs):
        super(CreateTrackView, self).__init__(**kwargs)

        self.session = session_factory()

    def create_track(self, artist, title, record):
        if not artist or not artist.strip():
            return
    
        if not title or not title.strip():
            return

        if record is not None and not record.strip():   
            return

        track = Track(artist = artist, title = title, record = record)

        self.session.add(track)
        self.session.commit()        
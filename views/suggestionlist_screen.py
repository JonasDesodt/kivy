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
        self.data = [ ]

    def fetch(self):
        suggestions = (
            self.session.query(TrackRelationship)
            .filter(TrackRelationship.track_id1 == self.id)
            .options(joinedload(TrackRelationship.track2))
            .all()
        )

        self.data = [{'track_id': tr.track2.track_id, 'artist': tr.track2.artist, 'title': tr.track2.title, 'record': tr.track2.record} for tr in suggestions]
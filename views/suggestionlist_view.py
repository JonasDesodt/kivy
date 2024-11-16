from kivy.uix.recycleview import RecycleView
from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import sessionmaker, joinedload
from app_container import AppContainer
from models.track_relationship_model import TrackRelationship
from kivy.properties import NumericProperty

class SuggestionlistView(RecycleView):
    track_id = NumericProperty(None) 

    @inject
    def __init__(self, session_factory: sessionmaker = Provide[AppContainer.session_factory], **kwargs):
        super(SuggestionlistView, self).__init__(**kwargs)

        self.session = session_factory()
        
        self.bind(track_id=self.on_track_id)

    def on_track_id(self, instance, value):
        if value:
            self.fetch()

    def fetch(self):
        suggestions = (
            self.session.query(TrackRelationship)
            .filter(TrackRelationship.track_id1 == self.track_id)
            .options(joinedload(TrackRelationship.track2))
            .all()
        )

        self.data = [{
            'track_relationship_id': tr.track_relationship_id,
            'track_id': tr.track2.track_id, 
            'artist': tr.track2.artist, 
            'title': tr.track2.title, 
            'record': tr.track2.record,
            'update_callback': self.fetch} for tr in suggestions]
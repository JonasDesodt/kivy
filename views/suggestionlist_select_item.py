from kivy.uix.boxlayout import BoxLayout
from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import sessionmaker
from app_container import AppContainer
from models.track_relationship_model import TrackRelationship
class SuggestionlistSelectItem(BoxLayout):

    @inject
    def __init__(self, update_callback = None, session_factory: sessionmaker = Provide[AppContainer.session_factory], **kwargs):
        super().__init__(**kwargs)
        self.session = session_factory()
        
        self.update_callback = update_callback

    def create_track_relationship(self, track_id1, track_id2):
        if self.track_id2 is not None:
            new_track_relationship = TrackRelationship(track_id1=track_id1, track_id2=track_id2)

            self.session.add(new_track_relationship)
            self.session.commit()

        if self.update_callback:
            self.update_callback()
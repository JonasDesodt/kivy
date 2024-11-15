from kivy.uix.recycleview import RecycleView
from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import sessionmaker, joinedload
from app_container import AppContainer
from models.track_relationship_model import TrackRelationship

class SuggestionlistView(RecycleView):
    pass
    # @inject
    # def __init__(self, session_factory: sessionmaker = Provide[AppContainer.session_factory], **kwargs):
    #     super(SuggestionlistView, self).__init__(**kwargs)
    
    # def fetch(self):
    #     track_relationship_id = self.id

    #     test = 'flag'
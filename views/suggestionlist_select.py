from kivy.uix.recycleview import RecycleView
from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import sessionmaker, joinedload
from app_container import AppContainer
from models.track_model import Track
from kivy.properties import NumericProperty

class SuggestionlistSelect(RecycleView):
    track_id1 = NumericProperty(None) 

    @inject
    def __init__(self, session_factory: sessionmaker = Provide[AppContainer.session_factory], **kwargs):
        super(SuggestionlistSelect, self).__init__(**kwargs)

        self.session = session_factory()

        self.update_data()

        self.bind(track_id1=self.on_track_id)


    def on_track_id(self, instance, value):
        if value:
            self.update_data()

    def filter_tracks(self, filter_text):
        tracks = self.session.query(Track).filter(
            (Track.artist.ilike(f'%{filter_text}%')) |
            (Track.title.ilike(f'%{filter_text}%')) |
            (Track.record.ilike(f'%{filter_text}%'))
        ).all()

        # self.update_data()
        self.data = [{'track_id1': self.track_id1,
                    'track_id2': track.track_id,
                    'artist': track.artist,
                    'title': track.title,
                    'record': track.record} for track in tracks]
        
    def update_data(self):
        tracks = self.session.query(Track).all()

        self.data = [{'track_id1': self.track_id1,
                    'track_id2': track.track_id,
                    'artist': track.artist,
                    'title': track.title,
                    'record': track.record,
                    'update_callback': self.update_data  } for track in tracks]          

    def refresh_recycleview(self):
        self.update_data()
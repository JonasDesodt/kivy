from kivy.uix.recycleview import RecycleView
from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import sessionmaker, joinedload
from app_container import AppContainer
from create_database import Track

class TracklistView(RecycleView):
    @inject
    def __init__(self, session_factory: sessionmaker = Provide[AppContainer.session_factory], **kwargs):
        super(TracklistView, self).__init__(**kwargs)

        self.session = session_factory()

        tracks = self.session.query(Track).all()

        self.data = [{'track_id': track.track_id,
                      'artist': track.artist,
                      'title': track.title,
                      'record': track.record} for track in tracks]        
    
    def filter_tracks(self, filter_text):
        tracks = self.session.query(Track).filter(
            (Track.artist.ilike(f'%{filter_text}%')) |
            (Track.title.ilike(f'%{filter_text}%')) |
            (Track.record.ilike(f'%{filter_text}%'))
        ).all()

        self.data = [{'track_id': track.track_id,
                                'artist': track.artist,
                                'title': track.title,
                                'record': track.record} for track in tracks]
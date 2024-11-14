# https://pypi.org/project/inject/3.1.1/
# https://python-dependency-injector.ets-labs.org/ pip install dependency-injector

from kivy.app import App
from kivy.uix.scrollview import ScrollView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from kivy.uix.screenmanager import ScreenManager, Screen
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from create_database import Track, PlaylistEntry, Playlist
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
# create_and_seed_database()

# Create engine and session for SQLAlchemy
# engine = create_engine('sqlite:///playlist.db')
# Session = sessionmaker(bind=engine)
# session = Session()

class AppContainer(containers.DeclarativeContainer):
    # Define the engine provider as a Singleton, passing the URL as an argument
    engine = providers.Singleton(create_engine, 'sqlite:///playlist.db')
    
    # Create a session factory provider
    session_factory = providers.Singleton(sessionmaker, bind=engine)
    
    # Singleton for screen_manager
    screen_manager = providers.Singleton(ScreenManager)

class TracklistScreen(Screen):
    pass

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

class TracklistItem(BoxLayout):
    # track_id = None  # Track ID placeholder
    
    @inject
    def __init__(self, session_factory: sessionmaker = Provide[AppContainer.session_factory], **kwargs):
        super().__init__(**kwargs)
        self.track_id = kwargs.get('track_id', None)

        self.session = session_factory()
    
    def add_to_playlist(self, instance):
        if self.track_id is not None:
            # Create PlaylistEntry to add this track to playlist_id 1
            new_playlist_entry = PlaylistEntry(track_id=self.track_id, playlist_id=1)
            self.session.add(new_playlist_entry)
            self.session.commit()
            print(f"Track {self.track_id} added to Playlist 1.")
            print(f"{self.session.query(PlaylistEntry).all()}")


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

                # Call the update callback if it exists
                if self.update_callback:
                    self.update_callback()

class PlaylistView(RecycleView):
    @inject
    def __init__(self, session_factory: sessionmaker = Provide[AppContainer.session_factory], **kwargs):
        super(PlaylistView, self).__init__(**kwargs)

        self.session = session_factory()

        self.update_data()

    def update_data(self):
        playlistEntries = (
            self.session.query(PlaylistEntry)
            .filter(PlaylistEntry.playlist_id == 1)
            .options(joinedload(PlaylistEntry.track))
            .all()
        )

        # Pass the update callback function to each item
        self.data = [{
            'playlist_entry_id': playlistEntry.playlist_entry_id,
            'track_id': playlistEntry.track.track_id,
            'artist': playlistEntry.track.artist,
            'title': playlistEntry.track.title,
            'record': playlistEntry.track.record,
            'update_callback': self.update_data  # Callback to refresh the playlist view
        } for playlistEntry in playlistEntries]

    def refresh_recycleview(self):
        self.update_data()

class PlaylistScreen(Screen):
    pass

class MainScreen(Screen):
    def switch_screen(self, screen_name):
        screen_manager = self.ids.main_screen_manager
        screen_manager.current = screen_name
    
class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class MainScreenManager(ScreenManager):
        def switch_screen(self, screen_name):
            self.current = screen_name



# class PlaylistScreen(Screen):
#     def on_enter(self):
#         # Update the playlist view when the screen is shown
#         self.update_playlist_data()

#     def update_playlist_data(self):
#         # Ensure the playlist view updates its data
#         if hasattr(self.ids, 'playlist_view'):
#             self.ids.playlist_view.update_data()

# class TracksScreen(Screen):
#     pass

# class TrackRelationshipsScreen(Screen):
#     pass

# class MainScreen(BoxLayout):
#     def __init__(self, screen_manager, **kwargs):
#         super().__init__(**kwargs)        
#         self.screen_manager = screen_manager  
    
#     def switch_screen(self, screen_name):
#         self.screen_manager.current = screen_name



# class TrackItem(BoxLayout):
#     track_id = None  # Track ID placeholder
    
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.track_id = kwargs.get('track_id', None)
    
#     def add_to_playlist(self, instance):
#         if self.track_id is not None:
#             # Create PlaylistEntry to add this track to playlist_id 1
#             new_playlist_entry = PlaylistEntry(track_id=self.track_id, playlist_id=1)
#             session.add(new_playlist_entry)
#             session.commit()
#             print(f"Track {self.track_id} added to Playlist 1.")
#             print(f"{session.query(PlaylistEntry).all()}")

# class TracklistView(RecycleView):
#     def __init__(self, **kwargs):
#         super(TracklistView, self).__init__(**kwargs)

#         # Query all tracks from the database
#         tracks = session.query(Track).all()

#         # Pass the track data as a dictionary to the RecycleView
#         self.data = [{'track_id': track.track_id,
#                       'artist': track.artist,
#                       'title': track.title,
#                       'record': track.record} for track in tracks]

# class PlaylistItem(BoxLayout):
#     def __init__(self, update_callback=None, **kwargs):
#         super().__init__(**kwargs)
        
#         self.playlist_entry_id = kwargs.get('playlist_entry_id', None)
#         self.update_callback = update_callback  # Store the reference to the update callback

#     def remove_from_playlist(self, instance):
#         if self.playlist_entry_id is not None:
#             playlistEntry = session.query(PlaylistEntry).filter(PlaylistEntry.playlist_entry_id == self.playlist_entry_id).first()

#             if playlistEntry:
#                 session.delete(playlistEntry)
#                 session.commit()

#                 # Call the update callback if it exists
#                 if self.update_callback:
#                     self.update_callback()

# class PlaylistView(RecycleView):
#     def __init__(self, **kwargs):
#         super(PlaylistView, self).__init__(**kwargs)
#         self.update_data()

#     def update_data(self):
#         playlistEntries = (
#             session.query(PlaylistEntry)
#             .filter(PlaylistEntry.playlist_id == 1)
#             .options(joinedload(PlaylistEntry.track))
#             .all()
#         )

#         # Pass the update callback function to each item
#         self.data = [{
#             'playlist_entry_id': playlistEntry.playlist_entry_id,
#             'track_id': playlistEntry.track.track_id,
#             'artist': playlistEntry.track.artist,
#             'title': playlistEntry.track.title,
#             'record': playlistEntry.track.record,
#             'update_callback': self.update_data  # Callback to refresh the playlist view
#         } for playlistEntry in playlistEntries]

# class TrackRelationshipsView(RecycleView):
#     def __init__(self, **kwargs):
#         super(TrackRelationshipsView, self).__init__(**kwargs)

# class PlaylistApp(App):
#     def build(self):
#         self.container = AppContainer()

#         # Return the screen_manager as the root widget
#         return MainScreen()


# Assuming MainScreen, MainScrollView, and AppContainer are already defined
class PlaylistApp(App):
    def build(self):
        # Initialize the DI container
        self.container = AppContainer()

        self.container.wire(modules=[__name__])

        return MainScreen()  


    # def switch_screen(self, screen_name):
    #     self.root.ids.screen_manager.current = screen_name

    #     if screen_name == 'playlist':
    #         # Trigger the update when entering the playlist screen
    #         screen = self.root.ids.screen_manager.get_screen('playlist')
    #         screen.update_playlist_data()

    # def filter_tracks(self, filter_text):
    #     # Access tracklist_view inside the TracksScreen
    #     tracklist_view = self.root.ids.screen_manager.get_screen('tracks').ids.tracklist_view
    #     tracks = session.query(Track).filter(
    #         (Track.artist.ilike(f'%{filter_text}%')) |
    #         (Track.title.ilike(f'%{filter_text}%')) |
    #         (Track.record.ilike(f'%{filter_text}%'))
    #     ).all()

    #     # Update TracklistView's data with filtered results
    #     tracklist_view.data = [{'track_id': track.track_id,
    #                             'artist': track.artist,
    #                             'title': track.title,
    #                             'record': track.record} for track in tracks]

    # def on_stop(self):
    #     # Close the session when the app stops
    #     session.close()


if __name__ == '__main__':
    PlaylistApp().run() 









# https://pypi.org/project/inject/3.1.1/
# # https://python-dependency-injector.ets-labs.org/ pip install dependency-injector

# from kivy.app import App
# from kivy.lang import Builder
# from kivy.uix.recycleview import RecycleView
# from kivy.uix.scrollview import ScrollView
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, joinedload
# from create_database import Track
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.recycleboxlayout import RecycleBoxLayout
# from kivy.uix.label import Label
# from kivy.uix.button import Button
# from create_database import PlaylistEntry, create_and_seed_database
# from kivy.uix.screenmanager import ScreenManager, Screen
# from dependency_injector import containers, providers

# # create_and_seed_database()

# # Create engine and session for SQLAlchemy
# engine = create_engine('sqlite:///playlist.db')
# Session = sessionmaker(bind=engine)
# session = Session()

# class AppContainer(containers.DeclarativeContainer):
#     engine = providers.Singleton(create_engine('sqlite:///playlist.db'))
#     session_factory = providers.Singleton(sessionmaker, bind=engine)

#     screen_manager = providers.Singleton(ScreenManager)

# class PlaylistScreen(Screen):
#     def on_enter(self):
#         # Update the playlist view when the screen is shown
#         self.update_playlist_data()

#     def update_playlist_data(self):
#         # Ensure the playlist view updates its data
#         if hasattr(self.ids, 'playlist_view'):
#             self.ids.playlist_view.update_data()

# class TracksScreen(Screen):
#     pass

# class TrackRelationshipsScreen(Screen):
#     pass

# class MainScreen(BoxLayout):
#     pass

# class TrackItem(BoxLayout):
#     track_id = None  # Track ID placeholder
    
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.track_id = kwargs.get('track_id', None)
    
#     def add_to_playlist(self, instance):
#         if self.track_id is not None:
#             # Create PlaylistEntry to add this track to playlist_id 1
#             new_playlist_entry = PlaylistEntry(track_id=self.track_id, playlist_id=1)
#             session.add(new_playlist_entry)
#             session.commit()
#             print(f"Track {self.track_id} added to Playlist 1.")
#             print(f"{session.query(PlaylistEntry).all()}")

# class TracklistView(RecycleView):
#     def __init__(self, **kwargs):
#         super(TracklistView, self).__init__(**kwargs)

#         # Query all tracks from the database
#         tracks = session.query(Track).all()

#         # Pass the track data as a dictionary to the RecycleView
#         self.data = [{'track_id': track.track_id,
#                       'artist': track.artist,
#                       'title': track.title,
#                       'record': track.record} for track in tracks]

# class PlaylistItem(BoxLayout):
#     def __init__(self, update_callback=None, **kwargs):
#         super().__init__(**kwargs)
        
#         self.playlist_entry_id = kwargs.get('playlist_entry_id', None)
#         self.update_callback = update_callback  # Store the reference to the update callback

#     def remove_from_playlist(self, instance):
#         if self.playlist_entry_id is not None:
#             playlistEntry = session.query(PlaylistEntry).filter(PlaylistEntry.playlist_entry_id == self.playlist_entry_id).first()

#             if playlistEntry:
#                 session.delete(playlistEntry)
#                 session.commit()

#                 # Call the update callback if it exists
#                 if self.update_callback:
#                     self.update_callback()

# class PlaylistView(RecycleView):
#     def __init__(self, **kwargs):
#         super(PlaylistView, self).__init__(**kwargs)
#         self.update_data()

#     def update_data(self):
#         playlistEntries = (
#             session.query(PlaylistEntry)
#             .filter(PlaylistEntry.playlist_id == 1)
#             .options(joinedload(PlaylistEntry.track))
#             .all()
#         )

#         # Pass the update callback function to each item
#         self.data = [{
#             'playlist_entry_id': playlistEntry.playlist_entry_id,
#             'track_id': playlistEntry.track.track_id,
#             'artist': playlistEntry.track.artist,
#             'title': playlistEntry.track.title,
#             'record': playlistEntry.track.record,
#             'update_callback': self.update_data  # Callback to refresh the playlist view
#         } for playlistEntry in playlistEntries]

# class TrackRelationshipsView(RecycleView):
#     def __init__(self, **kwargs):
#         super(TrackRelationshipsView, self).__init__(**kwargs)

# class PlaylistApp(App):
#     def build(self):
#         playlist_view = PlaylistView(screen_manager=self.root)  

#         return MainScreen()

#     def switch_screen(self, screen_name):
#         self.root.ids.screen_manager.current = screen_name

#         if screen_name == 'playlist':
#             # Trigger the update when entering the playlist screen
#             screen = self.root.ids.screen_manager.get_screen('playlist')
#             screen.update_playlist_data()

#     def filter_tracks(self, filter_text):
#         # Access tracklist_view inside the TracksScreen
#         tracklist_view = self.root.ids.screen_manager.get_screen('tracks').ids.tracklist_view
#         tracks = session.query(Track).filter(
#             (Track.artist.ilike(f'%{filter_text}%')) |
#             (Track.title.ilike(f'%{filter_text}%')) |
#             (Track.record.ilike(f'%{filter_text}%'))
#         ).all()

#         # Update TracklistView's data with filtered results
#         tracklist_view.data = [{'track_id': track.track_id,
#                                 'artist': track.artist,
#                                 'title': track.title,
#                                 'record': track.record} for track in tracks]

#     def on_stop(self):
#         # Close the session when the app stops
#         session.close()


# if __name__ == '__main__':
#     PlaylistApp().run() 
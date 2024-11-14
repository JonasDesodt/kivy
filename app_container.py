from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from kivy.uix.screenmanager import ScreenManager

class AppContainer(containers.DeclarativeContainer):
    engine = providers.Singleton(create_engine, 'sqlite:///playlist.db')
    
    session_factory = providers.Singleton(sessionmaker, bind=engine)

    screen_manager = providers.Singleton(ScreenManager)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Integer
from db import engine, session

Base = declarative_base()

class Player(Base):
    __tablename__ = "player"
    id = Column(String, primary_key=True)
    aliases = relationship("Alias", back_populates="player")
    results = relationship("PlayerResult")
    
    @property
    def display_name(self):
        dn = session.query(Alias).filter(
            Alias.player_id == self.id
        ).order_by(Alias.count.desc()).first()

        return dn.name
    
    @property
    def wins(self):
        return session.query(
            PlayerResult
        ).filter(
            PlayerResult.player_id==self.id,
            PlayerResult.match_win==1
        ).with_entities(func.count()).scalar()
    
    @property
    def games_played(self):
        return session.query(
            PlayerResult
        ).filter(
            PlayerResult.player_id==self.id
        ).with_entities(func.count()).scalar()


class Alias(Base):
    __tablename__ = "alias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    player_id = Column(String, ForeignKey('player.id'))
    count = Column(Integer, default=1)

    player = relationship("Player", back_populates="aliases")


class Replay(Base):
    __tablename__ = "replay"
    id = Column(String, primary_key=True)
    rocket_league_id = Column(String, unique=True)
    playlist_id = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)

    players = relationship("PlayerResult", back_populates="replay")

class PlayerResult(Base):
    __tablename__ = "player_result"
    id = Column(Integer, autoincrement=True, primary_key=True)
    match_win = Column(Boolean, nullable=False, default=False)
    replay_id = Column(String, ForeignKey('replay.id'))
    player_id = Column(String, ForeignKey('player.id'))
    replay = relationship("Replay", back_populates="players")
    player = relationship("Player", back_populates="results")


Base.metadata.create_all(engine)

from typing import List
from statistics import mean
import trueskill
from sqlalchemy import Column, Float, String, func
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Integer
from schema.replay import Player as PlayerSchema

from db import engine, session

Base = declarative_base()

class Player(Base):
    __tablename__ = "player"
    id = Column(String, primary_key=True)
    mu = Column(Float)
    sigma = Column(Float)

    aliases = relationship("Alias", back_populates="player", order_by="desc(Alias.count)")
    results = relationship("PlayerResult")
    
    @property
    def rating(self) -> trueskill.Rating:
        rating = trueskill.Rating(self.mu, self.sigma)
        return rating
    
    @rating.setter
    def rating(self, rating: trueskill.Rating):
        self.sigma = rating.sigma
        self.mu = rating.mu

    @property
    def display_name(self):
        # TODO: add an index on Alias.db for player_id
        dn = session.query(Alias).filter(
            Alias.player_id == self.id
        ).order_by(Alias.count.desc()).first()

        return dn.name
    
    @property
    def aka(self):
        return [f"{n.name} ({n.count})" for n in self.aliases]
    
    @staticmethod
    def from_name(name: str):
        alias = session.query(Alias).filter(Alias.name.ilike(f"{name}%")).order_by(Alias.count.desc()).first()
        try:
            return alias.player
        except Exception as e:
            print(e)
            return None


class Alias(Base):
    __tablename__ = "alias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    player_id = Column(String, ForeignKey('player.id'))
    count = Column(Integer, default=1)

    player: Player = relationship("Player", back_populates="aliases")


class Replay(Base):
    __tablename__ = "replay"
    id = Column(String, primary_key=True)
    replay_title = Column(String)
    match_hash = Column(Integer, unique=True)
    link = Column(String)
    rocket_league_id = Column(String, unique=True)
    playlist_id = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    duration = Column(Float)
    quality = Column(Float)
    winner_chance = Column(Float)
    player_count = Column(Integer)

    players = relationship("PlayerResult", back_populates="replay")

    @property
    def winners(self) -> List[Player]:
        return [p.player for p in self.players if p.match_win == True]
    
    @property
    def losers(self) -> List[Player]:
        return [p.player for p in self.players if p.match_win == False]

class PlayerResult(Base):
    __tablename__ = "player_result"
    id = Column(Integer, autoincrement=True, primary_key=True)
    match_win = Column(Boolean, nullable=False, default=False)
    replay_id = Column(String, ForeignKey('replay.id'))
    player_id = Column(String, ForeignKey('player.id'))
    score = Column(Integer)
    start_time = Column(Float)
    end_time = Column(Float)
    replay = relationship("Replay", back_populates="players")
    player = relationship("Player", back_populates="results")


Base.metadata.create_all(engine)

from app.bnet_retriever._plugin import Plugin
from app.bnet_retriever import api
from app.bnet_retriever.utils import reformat
from app.utils.db import Mongo
from typing import Dict
from bson import ObjectId
import logging
import pymongo

gamedata = api.get_gamedata()

logger = logging.getLogger(__name__)


class Profile(Plugin):
    def __init__(self, runner, func):
        super(Profile, self).__init__(runner)
        self._func = func
        # Lazy
        self._raw = None
        self._formatted = None

    @property
    def raw(self):
        if self._raw is None:
            self._raw = self._func(self)
        return self._raw

    @property
    def formatted(self):
        if self._formatted is None:
            self._formatted = {
                'career': reformat.detailed_mapping(gamedata, self.raw),
                'heroComparison': reformat.hero_comparison_mapping(gamedata, self.raw),
                'player': self.raw['player'],
            }
        return self._formatted

    def refresh(self):
        self._raw = None
        self._formatted = None

    def to_db_record(self):
        return {
            'user': self._id,
            **self.raw
        }

    def __gt__(self, other):
        # since it is gt, other will always be latest_profile,
        # if it is None, there's no record in db,
        # Init it
        if other.raw is None:
            return True
        return self.raw['lastUpdate'].__gt__(other.raw['lastUpdate'])

    @property
    def basic(self):
        data = self.raw['player']
        return {
            'battleTag': data['displayName'],
            'level': data['level'],
            'gamewon': data['gameWon'],
            'endorsement': data['endorsement'],
            'currentSR': data['ranked']['level'],
            'highestSR': data['ranked']['highestLevel']
        }


class DBProfile(Profile):
    def __init__(self, runner):
        def _retriever(self):
            return Mongo.db.profile.find_one({
                'user': self._id
            }, sort=[
                ('_id', pymongo.DESCENDING)
            ])
        super(DBProfile, self).__init__(runner, _retriever)


class RemoteProfile(Profile):
    def __init__(self, runner):
        def _retriever(self):
            return api.get_profile(self.root.credential.bnet_user_cred)
        super(RemoteProfile, self).__init__(runner, _retriever)

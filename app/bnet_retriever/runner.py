from app.bnet_retriever.profile import Profile, RemoteProfile, DBProfile
from app.bnet_retriever.credential import CredentialManager
from app.bnet_retriever.stat import CompetitiveStat
from app.utils.db import Mongo
from bson import ObjectId


class Runner:
    callbacks = []

    def __init__(self, username: str):
        record = Mongo.db.user.find_one({'username': username})
        if not record:
            raise Exception('No Such User')
        self.username: str = username
        self._id: ObjectId = record['_id']

        # Plugs
        # self.profile: Profile = Profile(self)
        self.new_profile = RemoteProfile(self)
        self.latest_profile = DBProfile(self)
        self.credential: CredentialManager = CredentialManager(self)
        self.competitive_stat = CompetitiveStat(self)

    def run(self):
        self.new_profile.refresh()
        self.latest_profile.refresh()
        if self.new_profile > self.latest_profile:
            Mongo.db.profile.insert(self.new_profile.to_db_record())
            self.competitive_stat.calc()

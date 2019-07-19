import json
import os
import time
from typing import Dict, Optional

from bson import ObjectId

from app.bnet_retriever._plugin import Plugin
from app.bnet_retriever.utils import serialize
from app.bnet_retriever.utils.login import login
from app.utils.db import Mongo


class CredentialManager(Plugin):
    def __init__(self, runner):
        super(CredentialManager, self).__init__(runner)
        self._bnet_user_cred: Optional[Dict] = None

    @property
    def raw_cred(self) -> Dict:
        return serialize.fromstr(Mongo.db.user.find_one({'_id': self._id})['credential'])

    @property
    def bnet_user_cred(self) -> str:
        # Here, self.last_updated_at records if the bnet_user_cred outdated ( 1 hr expiration)
        # Different from the lastUpdatedAt field in mongodb
        if self._bnet_user_cred is None or time.time() - self.last_updated_at > 60*55:
            bnet_user_cred, new_cred = login(self.raw_cred)
            self._bnet_user_cred = bnet_user_cred
            self.update_raw_cred(new_cred)
            self.last_updated_at = time.time()
        return self._bnet_user_cred

    def update_raw_cred(self, new_cred: Dict) -> None:
        Mongo.db.user.update_one({'_id': self._id}, {
            '$set': {
                'credential': serialize.tostr(new_cred),
            },
            '$currentDate': {
                'lastUpdatedAt': True
            }
        })

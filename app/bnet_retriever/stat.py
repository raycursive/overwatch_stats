from app.bnet_retriever._plugin import Plugin
from app.utils.db import Mongo
import logging

logger = logging.getLogger(__name__)


class CompetitiveStat(Plugin):

    def get_stats(self):
        return ({
            'gamePlayed': round(i['ranked']['所有英雄']['比赛场次']),
            'won': round(i['ranked']['所有英雄']['比赛胜利']),
            'lost': round(i['ranked']['所有英雄']['比赛战败']),
            'draw': round(i['ranked']['所有英雄']['比赛战平']),
            'skillRate': i['player']['ranked']['level'],
        } for i in (self.root.latest_profile.formatted['career'], self.root.new_profile.formatted['career']))

    def calc(self):
        old, new = self.get_stats()
        if old['gamePlayed'] == new['gamePlayed']:
            return
        try:
            assert new['gamePlayed'] - old['gamePlayed'] == 1, 'GameMissed'
            sr_diff = new['skillRate'] - old['skillRate']
            # basically, self.record(sign(sr_diff), sr_diff)
            # But with assertion
            if sr_diff > 0:
                assert new['won'] - old['won'] == 1, 'WonWrong'
                self.record(1, sr_diff, new)
            elif sr_diff < 0:
                assert new['lost'] - old['lost'] == 1, 'LostWrong'
                self.record(-1, sr_diff, new)
            elif sr_diff == 0:
                assert new['draw'] - old['draw'] == 1, 'DrawWrong'
                self.record(-1, sr_diff, new)
        except AssertionError as e:
            logging.error('[%s] calced error, [%s]', self._id, *e.args)

    def record(self, status, sr_diff, stats):
        Mongo.db.stats.insert({
            'user': self._id,
            'time': self.root.latest.raw['lastUpdate'],
            'gameStatus': status,
            'skillRateDifference': sr_diff,
            **stats
        })

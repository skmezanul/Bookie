"""Generate some stats on the bookmarks in the syste

Stats we want to track

- total bookmarks per day
- total # of tags in the system per day
- unique...not sure

- per user - number of bookmarks they have that day

- the popularity tracking numbers...let's show most popular by clicks? not
really stats

- outstanding invites
- invites sent but not accepted

# do the users thing as an hourly job, but assign a letter per hour of the day
# and run it that way. on hour 0 run A users, on hour 1 run B users, on hour
# 23 run xzy users.

"""
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Unicode

from bookie.models import Base
from bookie.models import DBSession
from bookie.models import BmarkMgr
from bookie.models import TagMgr


TOTAL_CT = 'user_bookmarks'
UNIQUE_CT = 'unique_bookmarks'
TAG_CT = 'total_tags'


class StatBookmarkMgr(object):
    """Handle our agg stuff for the stats on bookmarks"""

    @staticmethod
    def count_unique_bookmarks():
        """Count the unique number of bookmarks in the system"""
        total = BmarkMgr.count(distinct=True)
        stat = StatBookmark(attrib=UNIQUE_CT, data=total)
        DBSession.add(stat)

    @staticmethod
    def count_total_bookmarks():
        """Count the total number of bookmarks in the system"""
        total = BmarkMgr.count()
        stat = StatBookmark(attrib=TOTAL_CT, data=total)
        DBSession.add(stat)

    @staticmethod
    def count_total_tags():
        """Count the total number of tags in the system"""
        total = TagMgr.count()
        stat = StatBookmark(attrib=TAG_CT, data=total)
        DBSession.add(stat)


class StatBookmark(Base):
    """First stats we track are the counts of things.

    """
    __tablename__ = 'stats_bookmarks'

    id = Column(Integer, autoincrement=True, primary_key=True)
    tstamp = Column(DateTime, default=datetime.now)
    attrib = Column(Unicode(100), nullable=False)
    data = Column(Integer, nullable=False, default=0)

    def __init__(self, **kwargs):
        self.attrib = kwargs.get('attrib', 'unknown')
        self.data = kwargs.get('data', 0)

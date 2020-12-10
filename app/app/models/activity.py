
from models import db, CRUD
from helper import get_current, get_last_month


class Activity(db.Model, CRUD):

    id = db.Column(db.Integer, primary_key=True)

    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    target_id = db.Column(db.UnicodeText)
    target_type = db.Column(db.UnicodeText)

    activity_type = db.Column(db.UnicodeText, nullable=False)

    created_date = db.Column(db.DateTime, default=get_current)

    def in_this_month(self):
        current = get_current()
        return (current.month == self.created_date.month) and \
            (current.year == self.created_date.year)

    def in_last_month(self):
        last_month = get_last_month()
        return (last_month.month == self.created_date.month) and \
            (last_month.year == self.created_date.year)

    @classmethod
    def create(cls, activity_type, session=None, target=None):

        user_id = session['user']['id'] if 'user' in session else None

        if target:
            target_id = target.id
            target_type = target.__class__.__name__
        else:
            target_id = None
            target_type = None

        activity = cls(
            user=user_id, target_id=target_id,
            target_type=target_type, activity_type=activity_type
        )

        return activity.save()


exports = (Activity,)

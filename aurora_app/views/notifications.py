from flask import Blueprint, render_template

from aurora_app.models import Notification

mod = Blueprint('notifications', __name__, url_prefix='/notifications')


@mod.route('/table')
def table():
    notifications = Notification.query.order_by("created_at desc").all()
    return render_template('notifications/table.html',
                           notifications=notifications)

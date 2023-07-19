from models.models import User, Activity, Entry, db


def formation_list_activity(user_id):
    activities = db.session.query(Activity).filter(Activity.user_id == user_id).all()
    result_data = {}
    for activity in activities:
        result_data[activity.id] = activity.name
    return result_data
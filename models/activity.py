from models.models import User, Activity, Entry, db


def formation_list_activity(user_id):
    activities = db.session.query(Activity).filter(Activity.user_id == user_id).all()
    result_data = {}
    for activity in activities:
        result_data[activity.id] = activity.name
    return result_data


def get_related_activity_ids(activity_id):
    activity = db.session.get(Activity, activity_id)

    if not activity:
        return []

    related_ids = [a.id for a in activity.related_activities]
    related_ids.append(activity_id)

    return related_ids
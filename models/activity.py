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


def create_activity(user_id, name_activity, notification_text):
    try:
        new_activity = Activity(name=name_activity, user_id=user_id, notification_text=notification_text)
        db.session.add(new_activity)
        db.session.commit()

    except Exception as e:
        print("Ошибка при создании активности:", str(e))
        db.session.rollback()

    finally:
        db.session.close()


def delete_activity(activity_id):
    try:
        activity = db.session.query(Activity).get(activity_id)

        if activity:
            db.session.delete(activity)
            db.session.commit()


    except Exception as e:
        print("Ошибка при удалении записи:", str(e))

        db.session.rollback()


def update_activity(data_for_update, activity_id):
    new_name = data_for_update['name']
    new_notification_text = data_for_update['notification_text']
    # status = data_for_update['status']
    try:
        activity = db.session.query(Activity).get(activity_id)

        if activity:
            activity.name = new_name
            activity.notification_text = new_notification_text
            # activity.status = status

            db.session.commit()

    except Exception as e:
        print("Ошибка при обновлении записи:", str(e))
        db.session.rollback()

    finally:
        db.session.close()
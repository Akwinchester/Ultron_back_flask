from models.models import User, Activity, Entry, db


def formation_dataset_for_charts(activity_id):
    data = db.session.query(
        Entry.id,
        User.name.label('name_user'),
        Entry.amount,
        Entry.date_added
    ).join(Activity, Entry.activity_id == Activity.id).filter(
        Entry.activity_id == activity_id
    ).join(User, Activity.user_id == User.id).all()
    formatted_data = []

    for row in data:
        formatted_data.append({
            'id': row.id,
            'name': row.name_user,
            'amount': row.amount,
            'date_added': row.date_added
        })

    return formatted_data
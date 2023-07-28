from models.models import User, Activity, Entry, db
from models.activity import get_related_activity_ids

def formation_dataset_for_charts_only_you(activity_id):
    data = db.session.query(
        Entry.id.label('id_entery'),
        User.name.label('name_user'),
        User.id.label('id_user'),
        Entry.amount,
        Entry.date_added,
        Entry.description
    ).join(Activity, Entry.activity_id == Activity.id).filter(
        Entry.activity_id == activity_id
    ).join(User, Activity.user_id == User.id).all()
    formatted_data = []

    for row in data:
        formatted_data.append({
            'id_user': row.id_user,
            'id_entery': row.id_entery,
            'name': row.name_user,
            'amount': row.amount,
            'date_added': str(row.date_added),
            'description': row.description
        })

    # formatted_data = randomdataset(20)
    return formatted_data

def formation_dataset_for_charts_rating(activity_id):
    activity_ids = get_related_activity_ids(activity_id)

    data = (
        db.session.query(
            Entry.id.label('id_entery'),
            User.name.label('name_user'),
            User.id.label('id_user'),
            Entry.amount,
            Entry.date_added,
            Entry.description
        )
        .join(Activity, Entry.activity_id == Activity.id)
        .filter(Entry.activity_id.in_(activity_ids))
        .join(User, Activity.user_id == User.id)
        .all()
    )

    formatted_data = []

    for row in data:
        formatted_data.append({
            'id_user': row.id_user,
            'id_entery': row.id_entery,
            'name': row.name_user,
            'amount': row.amount,
            'date_added': str(row.date_added),
            'description': row.description
        })
        print(formatted_data)
    return formatted_data






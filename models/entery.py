from models.models import User, Activity, Entry, db


def formation_dataset_for_charts(activity_id):
    data = db.session.query(
        Entry.id.label('id_entery'),
        User.name.label('name_user'),
        User.id.label('id_user'),
        Entry.amount,
        Entry.date_added
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
            'date_added': str(row.date_added)
        })

    # formatted_data = randomdataset(20)
    return formatted_data









from datetime import datetime, timedelta
from random import randint


def randomdataset(size):
    today = datetime.now()
    data = []

    for i in range(size):
        date = today - timedelta(days=i)
        amount = randint(30, 100)

        data.append({
            "id_user": randint(1, 3),
            "id_entery": i + 1,
            "name": "Test User",
            "amount": amount,
            "date_added": date.isoformat()[:10]
        })

    return data




import re
from models.models import User, Activity, Entry, db
from models.activity import get_related_activity_ids
from flask import session

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

    merge_formatted_data = merge_entries(formatted_data)
    return merge_formatted_data


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

    merge_formatted_data = merge_entries(formatted_data)
    return merge_formatted_data


def merge_entries(data):
    merged_data = {}

    for entry in data:
        key = (entry['id_user'], entry['date_added'])
        if key not in merged_data:
            merged_data[key] = {
                'id_user': entry['id_user'],
                'id_entery': entry['id_entery'],
                'name': entry['name'],
                'amount': entry['amount'],
                'date_added': entry['date_added'],
                'description': f"Тренировка 1: {entry['amount']}  ({entry['description']})<br>"
            }
        else:
            merged_data[key]['amount'] += entry['amount']

            pattern = r"Тренировка (\d+):"
            matches = re.findall(pattern, merged_data[key]['description'])
            if matches:
                idx = int(matches[-1]) + 1
            else:
                idx = 2
            merged_data[key]['description'] += f"Тренировка {idx}: {entry['amount']} ({entry['description']})<br>"

    return list(merged_data.values())


def delete_entry(id_entry):
    entry = db.session.get(Entry, id_entry)

    user = db.session.query(User.id) \
    .join(Activity, User.id == Activity.user_id) \
    .join(Entry, Activity.id == Entry.activity_id) \
    .filter(Entry.id == id_entry) \
    .first()

    if entry and str(user.id) == str(session['_user_id']):
        db.session.delete(entry)
        db.session.commit()
        db.session.close()
        return "Запись успешно удалена"
    else:
        return "Нельзя удалить эту запись"


def edit_entry(data, id_entry):
    entry = db.session.get(Entry, id_entry)

    user = db.session.query(User.id) \
    .join(Activity, User.id == Activity.user_id) \
    .join(Entry, Activity.id == Entry.activity_id) \
    .filter(Entry.id == id_entry) \
    .first()

    if entry and str(user.id) == str(session['_user_id']):
        if data['amount'] != '':
            entry.amount = data['amount']
        if data['date_added'] != "":
            entry.date_added = data['date_added']
        if data['description'] != '':
            entry.description = data['description']

        db.session.commit()
        db.session.close()
        return "Запись успешно отредактированна"
    else:
        return "Нельзя редактировать эту запись"


def create_entry( data, activity_id):
    entry = Entry(amount=data['amount'], description=data['description'], date_added=data['date_added'], activity_id=data['activity_id'])
    db.session.add(entry)
    return 'Запись успешно создана'
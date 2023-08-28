import re
from models.models import User, Activity, Entry, db
from models.activity import get_related_activity_ids
from flask import session
from datetime import timedelta


def formation_dataset_for_charts_only_you(activity_id):
    data = db.session.query(
        Entry.id.label('entry_id'),
        User.username.label('user_name'),
        User.id.label('user_id'),
        Entry.amount,
        Entry.date_added,
        Entry.description
    ).join(Activity, Entry.activity_id == Activity.id).filter(
        Entry.activity_id == activity_id
    ).join(User, Activity.user_id == User.id).all()


    # merge_formatted_data = merge_entries(formatted_data)
    if len(data) > 0:
        dataset = make_dataset(data)
    else:
        dataset = []
    return dataset


def formation_dataset_for_charts_rating(activity_id):
    activity_ids = get_related_activity_ids(activity_id)

    data = (
        db.session.query(
            Entry.id.label('id_entry'),
            User.username.label('name_user'),
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
            'id_entry': row.id_entry,
            'name': row.name_user,
            'amount': row.amount,
            'date_added': str(row.date_added),
            'description': row.description
        })

    # merge_formatted_data = merge_entries(formatted_data)
    if len(data) > 0:
        dataset = make_dataset(data)
    else:
        dataset = []

    return dataset


def merge_entries(data):
    merged_data = {}

    for entry in data:
        key = (entry['id_user'], entry['date_added'])
        if key not in merged_data:
            merged_data[key] = {
                'id_user': entry['id_user'],
                'id_entry': entry['id_entry'],
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
        return "Record successfully edited"
    else:
        return "This entry cannot be edited"


def create_entry( data, activity_id):
    entry = Entry(amount=data['amount'], description=data['description'], date_added=data['date_added'], activity_id=activity_id)
    db.session.add(entry)
    db.session.commit()
    db.session.close()
    return 'Запись успешно создана'


def make_dataset(data):

    dataset = {
        "date": [],
        "amount": {},
        "entry_id": {},
        "description": {},
        "user_id": [],
        "name": {}
    }

    real_date = []

    start_date = min(row[4] for row in data)
    end_date = max(row[4] for row in data)

    delta = end_date - start_date
    dates = [start_date + timedelta(days=i) for i in range(delta.days + 1)]

    dataset["date"] = [d.strftime("%m-%d") for d in dates]

    for row in data:
        real_date.append(row[4])
        row = list(row)
        row[4] = 1
        user_id = row[2]
        if user_id not in dataset["entry_id"]:
            dataset["entry_id"][user_id] = ['' for i in dates]
            dataset["description"][user_id] = ['' for i in dates]
        if user_id not in dataset["user_id"]:
            dataset["user_id"].append(user_id)
            dataset["name"][user_id] = row[1]
        dataset['amount'][user_id] = [0 for i in dates]
    dataset = enter_data(dataset, data, real_date, dates)
    sorted(dataset['user_id'])
    return dataset


def enter_data(dataset, data, real_date, date_line):
    for date in date_line:
        if date in real_date:
            for row in data:
                if row[4] == date:
                    for user in dataset['user_id']:
                        if user == row[2]:
                            dataset['amount'][user][date_line.index(date)] = row[3]
                            dataset['description'][user][date_line.index(date)] = row[5]
                            dataset['entry_id'][user][date_line.index(date)] = row[0]
    return dataset

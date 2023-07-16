from models.models import Entry

def formation_dataset_for_charts(activity_id):
    entries = Entry.query.filter(Entry.activity_id == activity_id).all()
    data_for_charts = []
    for entery in entries:
        entery_object = {}
        entery_object['date'] = entery.date_added
        entery_object['amount'] = entery.amount
        data_for_charts.append(entery_object)
    return data_for_charts
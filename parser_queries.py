# admin file
# used https://medium.com/@cbrannen/importing-data-into-firestore-using-python-dce2d6d3cd51 as a reference

import firebase_connection as fc
from google.cloud.firestore_v1 import FieldFilter

# Firebase Connection Setup
cred, app, store = fc.fb_conn()


def greater_than_val_not_inc(item, value):
    return_list = []
    ref = store.collection(u'state-data')
    docs = ref.where(filter=FieldFilter(item, ">", value)).stream()
    for doc in docs:
        return_list.append(doc.to_dict())
    return return_list


def greater_than_val_inc(item, value):
    return_list = []
    ref = store.collection(u'state-data')
    docs = ref.where(filter=FieldFilter(item, ">=", value)).stream()
    for doc in docs:
        return_list.append(doc.to_dict())
    return return_list


def equal_to_val(item, value):
    return_list = []
    ref = store.collection(u'state-data')
    docs = ref.where(filter=FieldFilter(item, "==", value)).stream()
    for doc in docs:
        return_list.append(doc.to_dict())
    return return_list


def less_than_val_inc(item, value):
    return_list = []
    ref = store.collection(u'state-data')
    docs = ref.where(filter=FieldFilter(item, "<=", value)).stream()
    for doc in docs:
        return_list.append(doc.to_dict())
    return return_list


def less_than_val_not_inc(item, value):
    return_list = []
    ref = store.collection(u'state-data')
    docs = ref.where(filter=FieldFilter(item, "<", value)).stream()
    for doc in docs:
        return_list.append(doc.to_dict())
    return return_list


dct1 = (equal_to_val(u'state', "Kentucky"))
print(dct1)

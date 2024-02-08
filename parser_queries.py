# admin file
# used https://medium.com/@cbrannen/importing-data-into-firestore-using-python-dce2d6d3cd51 as a reference

import firebase_connection as fc
from google.cloud.firestore_v1 import FieldFilter

# Firebase Connection Setup
cred, app, store = fc.fb_conn()

def do_query(item, symbol, value):
    symbol = symbol.strip()
    return_list = []
    ref = store.collection(u'state-data')
    docs = ref.where(filter=FieldFilter(item, symbol, value)).stream()
    for doc in docs:
        return_list.append(doc.to_dict())
    return return_list


dct1 = (do_query('median_age', ' < ', 35))
print(dct1)

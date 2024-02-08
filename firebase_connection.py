# firebase connector for connection code used in both admin and parser

import firebase_admin
from firebase_admin import credentials, firestore


def fb_conn():
    cred = credentials.Certificate("firebase-adminsdk-key.json")
    app = firebase_admin.initialize_app(cred)
    store = firestore.client()
    return [cred, app, store]

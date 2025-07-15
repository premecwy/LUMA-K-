import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("lumaai-12b32-firebase-adminsdk-fbsvc-9a122f066b.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

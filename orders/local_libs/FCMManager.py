import firebase_admin
from firebase_admin import credentials, messaging
import os

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"push-notification-af24c-firebase-adminsdk-4dms3-11d96d19d7.json")
cred = credentials.Certificate(file_path)
firebase_admin.initialize_app(cred)

def send_push(message, title, registraton_token, dataObject=None):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=message,
        ),
        data=dataObject,
        tokens=registraton_token
    )

    response = messaging.send_multicast(message)
    
    print("Successfully sent message: ", response)

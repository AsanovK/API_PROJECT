    
    
    
from django.conf import settings
from config.celery import app

@app.task
def send_activation_sms(phone, activation_code):
    from twilio.rest import Client
    client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f'htttp://127.0.0.1:8000/account/activate/{activation_code}',
        from_=settings.TWILIO_NUMBER,
        to = phone
    )
    print(message.sid)
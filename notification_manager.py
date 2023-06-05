from twilio.rest import Client

TWILIO_SID = "AC87b8db5871cb8c926a53470e8967c08d"
TWILIO_AUTH_TOKEN = "f64f660a3714ff1d87c3d768e70b4a19"
TWILIO_VIRTUAL_NUMBER = "+15673612814"
TWILIO_VERIFIED_NUMBER = "+886972022143"


class NotificationManager:
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )
        # Prints if successfully sent.
        print(message.sid)

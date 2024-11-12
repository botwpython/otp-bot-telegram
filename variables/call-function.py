from twilio.rest import Client
import os
from app.utils import text_to_speech, record_call
from app.models import CallLog
# this code is totally example for otp bot's algorithm, it's very short example of call function, so it's wouldn't work if u thinking the try to this code for run it now.

class CallService:
    def __init__(self, user, otp):
        self.user = user
        self.otp = otp
        self.client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        self.call_record = None

    def initiate_call(self):
        # Using Twilio API to make the call on otp bot
        try:
            call = self.client.calls.create(
                to=self.user.phone,
                from_=os.getenv("TWILIO_PHONE_NUMBER"),
                url="http://yourserver.com/handle-otp-call",
                method="GET"
            )
            self.call_record = CallLog(user_id=self.user.id, call_sid=call.sid)
            self.save_call_record()
        except Exception as e:
            print(f"Error initiating call: {e}")
    
    def save_call_record(self):
        if self.call_record:
            # Save the call record to the otp bot user's database
            CallLog.save(self.call_record)

    def play_otp_message(self):
        # Use Twilio to deliver a TTS message or a pre-recorded OTP message from otp bot scripts
        otp_message = f"Your OTP is {self.otp}. Please enter it to verify your identity."
        message = text_to_speech(otp_message)  # convert text to speech
        # Send the message as audio via Twilio (or use a pre-recorded message)
        self.client.calls.create(
            to=self.user.phone,
            from_=os.getenv("TWILIO_PHONE_NUMBER"),
            twiml=f'<Response><Say>{otp_message}</Say></Response>'
        )

    def record_user_response(self):
        # Record the user's response (press key for OTP verification)
        pass  # You can record the press or interaction based on your needs

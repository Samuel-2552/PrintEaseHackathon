from twilio.rest import Client
import random

def send_otp(to_number):
    # Your Twilio account SID and auth token
    account_sid = 'AC0d4c5f5ddc683a69f2dc0bb95e7304d4'
    auth_token = 'bd7c3b87d7f437b9c4b6eb2558ccbe6c'

    # Twilio phone number
    from_number = '+19786789175'

    # Generate a random OTP
    otp = str(random.randint(1000,9999))

    # SMS message
    message = 'Your OTP for PrintEase Verification is: ' + otp

    try:
        # Send the SMS message
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to=to_number,
            from_=from_number,
            body=message
        )

        print('SMS sent! Message SID:', message.sid)
    except Exception as e:
        print(e)
        print('Something went wrong...')

# Example usage
send_otp('+918279598383')

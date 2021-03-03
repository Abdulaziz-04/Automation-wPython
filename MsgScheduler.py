import datetime
from decouple import config
from twilio.rest import Client
from time import sleep

# Setup Twilio Client(Twiilio API)
client = Client(config('SID'), config('AUTH'))
# Get target date and time
target = input(
    'Enter your Date and Time seperated by spaces in format YYYY MM DD HH MM : \n')
year, month, day, hour, minute = map(int, target.split())
# Formatting and arranging...
target_date = datetime.datetime(
    year=year, month=month, day=day, hour=hour, minute=minute)
# Get the Text Message
message = input('Enter the text you want to send : \n')
# Get the input number
try:
    receiver = config('TO')
except:
    receiver = ""
    receiver += 'whatsapp:'
    receiver += input('Enter target whatsapp number(with country code)(Verification required) : \n')
print("Task Scheduled ... \n")
while True:
    # Get current time
    current_time = datetime.datetime.now()
    # If Elapse is high,make the program go to sleep...
    elapse = target_date - current_time
    if(elapse > datetime.timedelta(minutes=2)):
        sleep(elapse.total_seconds()-60)
    if(target_date < current_time):
        # Sending the message
        send_message = client.messages.create(
            body=message, from_=config('FROM'), to=config('TO'))
        break
print('Message Sent Succesfully! \n')

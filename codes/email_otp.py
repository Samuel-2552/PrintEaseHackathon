import math
import random
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

digits = "0123456789"
OTP = ""
for i in range(6):
    OTP += digits[math.floor(random.random() * 10)]

otp = OTP + " is your OTP"
msg = MIMEMultipart()
msg['From'] = 'PrintEase Verification'
msg['To'] = input("Enter your email: ")
msg['Subject'] = 'OTP Verification'
msg.attach(MIMEText(otp, 'plain'))

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login("201501503@rajalakshmi.edu.in", "RECLE@2021")
s.sendmail(msg['From'], msg['To'], msg.as_string())
a = input("Enter Your OTP >>: ")
if a == OTP:
    print("Verified")
else:
    print("Please Check your OTP again")
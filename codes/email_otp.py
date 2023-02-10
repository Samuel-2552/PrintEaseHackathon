import os
import math
import random
import smtplib

digits="0123456789"
OTP=""
for i in range(6):
    OTP+=digits[math.floor(random.random()*10)]
otp = OTP + " is your OTP"
msg= otp

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login("201501502@rajalakshmi.edu.in", "##")
emailid = input("Enter your email: ")
s.sendmail('201501502@rajalakshmi.edu.in',emailid,msg)
a = input("Enter Your OTP >>: ")
if a == OTP:
    print("Verified")
else:
    print("Please Check your OTP again")
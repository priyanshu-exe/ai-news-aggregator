from dotenv import load_dotenv
import os, smtplib

load_dotenv()
email = os.getenv('MY_EMAIL')
pw = os.getenv('APP_PASSWORD')
print('MY_EMAIL present:', bool(email))
print('APP_PASSWORD present:', 'set' if pw else 'missing')
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as s:
        s.login(email, pw)
    print('SMTP login OK')
except Exception as e:
    print('SMTP login failed:', repr(e))

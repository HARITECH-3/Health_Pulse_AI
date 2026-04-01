import requests
import re
import os

response = requests.post("https://api.nodemailer.com/user")
if response.status_code == 200:
    data = response.json()
    user = data['user']
    password = data['pass']
    
    env_path = 'c:\\Users\\Aravind\\Downloads\\disease_chatbot\\disease_chatbot\\ncd_health_chatbot\\backend\\.env'
    with open(env_path, 'r') as f:
        content = f.read()
    
    # Replace SMTP settings
    content = re.sub(r'SMTP_SERVER=.*', 'SMTP_SERVER=smtp.ethereal.email', content)
    content = re.sub(r'SMTP_PORT=.*', 'SMTP_PORT=587', content)
    content = re.sub(r'SMTP_USERNAME=.*', f'SMTP_USERNAME={user}', content)
    content = re.sub(r'SMTP_PASSWORD=.*', f'SMTP_PASSWORD={password}', content)
    
    with open(env_path, 'w') as f:
        f.write(content)
        
    print(f"SUCCESS: Fake Email Created! -> {user}")
    print(f"You can view sent emails by logging in at: https://ethereal.email/login")
else:
    print("Failed to get Ethereal account.")

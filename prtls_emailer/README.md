# 📧 Protellus Emailer - A Reusable Django Email Service

Emailer is a **Django package** that provides an API-based email service with **rate-limiting, retry logic, and template rendering**. It integrates with external email services using an API key and supports **plain text & HTML emails**.

## 🚀 Features
✅ **Send emails with API integration**  
✅ **Throttling & Rate-Limiting** (Prevent API overuse)  
✅ **Retry Mechanism** for failed requests (e.g., rate limit exceeded)  
✅ **Supports HTML and Plain Text Emails**  
✅ **Automatically converts HTML to Plain Text for compatibility**  
✅ **Renders Django Templates for Emails**  
✅ **Django REST Framework Serializer & API Endpoint**  

---

### 🛠️ Installation

pip install git+https://github.com/protellus/prtls-emailer.git

#### Or install locally in development:

pip install -e /path/to/prtls-emailer

### ⚙️ Configuration

Add "prtls_emailer" to INSTALLED_APPS in settings.py:

EMAIL_API_KEY = "your-api-key-here"
EMAIL_DEFAULT_SENDER = "no-reply@example.com"
EMAIL_DEFAULT_FROM_NAME = "My Service"
EMAIL_DEFAULT_REPLY_TO = "support@example.com"
EMAIL_ALERT_RECIPIENTS = "alerts@example.com"

### 📤 Sending an Email (Usage)

from emailer.services import EmailService

email_service = EmailService()
response = email_service.send(
    to_address="recipient@example.com",
    subject="Hello from Django!",
    html_body="<h1>Welcome to Our Service</h1><p>This is a test email.</p>"
)

### Using a Django Template

response = email_service.render_and_send(
    to_address="recipient@example.com",
    subject="Welcome!",
    template_name="emails/welcome.html",
    context={"username": "JohnDoe"}
)

### 🛠️ API Endpoint (Django REST Framework)

POST /api/send-email/

#### 📤 Sample Request

{
    "to_address": "recipient@example.com",
    "from_address": "no-reply@example.com",
    "subject": "Hello from API",
    "html_body": "<h1>Welcome!</h1>"
}

### 📥 Response

{
    "message": "Email sent successfully!",
    "api_response": { "id": "12345", "status": "sent" }
}

### 📝 Serializer for Validation

from emailer.serializers import EmailSendSerializer

data = {
    "to_address": "recipient@example.com",
    "subject": "Test Email",
    "html_body": "<h1>Hello</h1>"
}

serializer = EmailSendSerializer(data=data)
if serializer.is_valid():
    print("Valid email data!")
else:
    print(serializer.errors)

### ⚡ Error Handling & Logging

- If EMAIL_API_KEY is missing, the service raises an error.
- If rate limits are exceeded, it waits and retries automatically.
- Logs warnings for missing configuration settings.
import logging
import requests
import time
import html2text
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
from prtls_utils.utils import get_setting

logger = logging.getLogger(__name__)

class EmailBaseService:
    BASE_URL = "https://api.emailit.com/v1"

    def __init__(self):
        self._headers = None
        self._api_key = get_setting("EMAIL_API_KEY")
        if not self._api_key:
            logger.error("EMAIL_API_KEY is required for EmailService.")
            raise ValueError("EMAIL_API_KEY is required for EmailService.")

        # ✅ Throttling Variables
        self.max_requests_per_minute = 60  # Customize rate limit if needed
        self.request_interval = 60 / self.max_requests_per_minute  # Time between requests

        self.last_request_time = 0  # Track last request time

    @property
    def headers(self):
        if self._headers is None:
            self._headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            }
        return self._headers

    def _throttle(self):
        """ Ensures API requests do not exceed rate limits. """
        elapsed_time = time.time() - self.last_request_time
        if elapsed_time < self.request_interval:
            wait_time = self.request_interval - elapsed_time
            logger.debug(f"Throttling: Waiting {wait_time:.2f} seconds before next request.")
            time.sleep(wait_time)

    def _handle_response(self, response: requests.Response):
        """ Handles API responses and implements retry logic for 429 errors. """
        try:
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx/5xx)

            # ✅ Reset Last Request Time on Successful Request
            self.last_request_time = time.time()
            return response.json() if response.text else None

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 5))  # Default retry time if not provided
                logger.warning(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)
                return self._retry_last_request(response.request)  # Retry the request
            else:
                logger.error(f"Email API request failed: {e} - Response: {response.text}")
                raise

    def _retry_last_request(self, request: requests.PreparedRequest):
        """ Retries the last request after a delay due to rate limiting. """
        time.sleep(5)  # Default retry delay
        logger.info(f"Retrying request: {request.method} {request.url}")

        session = requests.Session()
        response = session.send(request)
        return self._handle_response(response)

    def post(self, endpoint, data):
        """ Sends a POST request to the Email API with throttling. """
        self._throttle()
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def get(self, endpoint, params=None):
        """ Sends a GET request to the Email API with throttling. """
        self._throttle()
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        return self._handle_response(response)

    def put(self, endpoint, data):
        """ Sends a PUT request to the Email API with throttling. """
        self._throttle()
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.put(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def delete(self, endpoint):
        """ Sends a DELETE request to the Email API with throttling. """
        self._throttle()
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.delete(url, headers=self.headers)
        return self._handle_response(response)


class EmailService(EmailBaseService):
    """ Service for sending emails using EmailBaseService. """
    def __init__(self):
        super().__init__()
        self._default_sender = get_setting("EMAIL_DEFAULT_SENDER")
        self._default_from_name = get_setting("EMAIL_DEFAULT_FROM_NAME")
        self._default_reply_to = get_setting("EMAIL_DEFAULT_REPLY_TO")

    def send(self, to_address: str, from_address: str = None, from_name: str = None,
                   reply_to_address: str = None, cc_address: str = "", subject: str = "",
                   html_body: str = "") -> dict:
        """
        Sends an email with the specified details.

        Args:
            to_address (str): Recipient email address (comma-separated for multiple).
            from_address (str, optional): Sender email address.
            from_name (str, optional): Sender's name.
            reply_to_address (str, optional): Reply-to email address.
            cc_address (str, optional): CC email address.
            subject (str, optional): Email subject.
            html_body (str, optional): HTML body content.

        Returns:
            dict: API response.
        """

        from_address = from_address or self._default_sender
        from_name = from_name or self._default_from_name or ""
        reply_to_address = reply_to_address or self._default_reply_to or from_address

        if not to_address or not from_address:
            logger.error("Missing required parameters: 'to_address' or 'from_address'.")
            raise ValueError("Recipient (to_address) and sender (from_address) must be provided.")

        sender = f"{from_name} <{from_address}>" if from_name else from_address

        payload = {
            "from": sender,
            "to": to_address.split(",") if "," in to_address else to_address,  # Handle multiple recipients
            "reply_to": reply_to_address if reply_to_address else None,
            "subject": subject or "No Subject",
            "html": html_body or "",
            "text": html2text.html2text(html_body) if html_body else "",
            "cc": cc_address if cc_address else None,
            "headers": {},
        }
        
        try:
            logger.info(f"Sending email to {to_address} from {sender}.")
            response = self.post("emails", payload)
            logger.debug(f"Email API Response: {response}")
            return response
        except Exception as e:
            logger.exception(f"Failed to send email to {to_address}: {e}")
            raise RuntimeError(f"Error sending email to {to_address}.") from e

    def render(self, template_name: str, context: dict = None) -> str:
        """
        Renders an email template with the given context.

        Args:
            template_name (str): The name of the template.
            context (dict, optional): Context data.

        Returns:
            str: Rendered HTML content.
        """
        if not template_name:
            raise ValueError("Template name must be provided.")

        context = context or {}  # Ensure context is always a dictionary

        try:
            return render_to_string(template_name, {"data": context})
        except TemplateDoesNotExist:
            logger.error(f"Template '{template_name}' not found.")
            raise ValueError(f"Template '{template_name}' not found.")
        except Exception as e:
            logger.exception(f"Error rendering template '{template_name}': {e}")
            raise RuntimeError("Error processing your request.") from e

    def render_and_send(self, to_address: str, from_address: str = None, from_name: str = None,
                              reply_to_address: str = None, cc_address: str = "", subject: str = "",
                              template_name: str = "", context: dict = None) -> dict:
        """
        Renders an email template and sends the email.

        Args:
            to_address (str): Recipient email address.
            from_address (str, optional): Sender email address.
            from_name (str, optional): Sender's name.
            reply_to_address (str, optional): Reply-to email address.
            cc_address (str, optional): CC email address.
            subject (str, optional): Email subject.
            template_name (str, optional): Template name.
            context (dict, optional): Template context.

        Returns:
            dict: API response.
        """
        if not template_name:
            raise ValueError("Template name must be provided.")

        context = context or {}  # Ensure context is always a dictionary

        logger.debug(f"Rendering and sending email to {to_address} from {from_address}.")
        logger.debug(f"Template: {template_name}, Context: {context}")

        try:
            html_body = self.render(template_name, context)
            return self.send(to_address, from_address, from_name, reply_to_address, cc_address, subject, html_body)
        except Exception as e:
            logger.exception(f"Failed to render and send email to {to_address}: {e}")
            raise RuntimeError(f"Error rendering and sending email to {to_address}.") from e

    def send_system_alert(self, subject: str, message: str) -> dict:
        """
        Sends a system alert email to the configured recipients.

        Args:
            subject (str): Email subject.
            message (str): Email message.

        Returns:
            dict: API response.
        """
        recipients = get_setting("EMAIL_ALERT_RECIPIENTS")

        # ✅ Ensure recipients exist, fallback to default
        if not recipients:
            recipients = "michael.britton@protellus.ca"
            message = f"EMAIL_ALERT_RECIPIENTS not configured. Alert: {message}"
            logger.warning("EMAIL_ALERT_RECIPIENTS not set. Using fallback recipient.")

        logger.info(f"Sending system alert to: {recipients}")
        
        return self.send(
            to_address=recipients,
            from_address=self._default_sender,
            subject=f"Alert: {subject}",
            html_body=message,
        )

    
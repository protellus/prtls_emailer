import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from prtls_emailer.serializers import EmailSendSerializer
from prtls_emailer.services import EmailService 

logger = logging.getLogger(__name__)

class SendEmailView(APIView):
    """
    API endpoint to test email sending.
    """

    def post(self, request):
        serializer = EmailSendSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            email_service = EmailService()

            try:
                logger.info(f"Sending email to {data['to_address']} from {data['from_address']}.")
                logger.info('Email data: %s', data)
                # Determine whether to send with template or raw HTML
                if data.get("template_name"):
                    logger.info(f"Rendering email template: {data['template_name']}.")
                    logger.debug(f"Context: {data.get('context', {})}")
                    response = email_service.render_and_send(
                        to_address=data["to_address"],
                        from_address=data["from_address"],
                        from_name=data.get("from_name", ""),
                        reply_to_address=data.get("reply_to_address", ""),
                        cc_address=data.get("cc_address", ""),
                        subject=data.get("subject", ""),
                        template_name=data["template_name"],
                        context=data.get("context", {})
                    )
                else:
                    response = email_service.send(
                        to_address=data["to_address"],
                        from_address=data["from_address"],
                        from_name=data.get("from_name", ""),
                        reply_to_address=data.get("reply_to_address", ""),
                        cc_address=data.get("cc_address", ""),
                        subject=data.get("subject", ""),
                        html_body=data["html_body"]
                    )

                return Response({"message": "Email sent successfully!", "api_response": response}, status=status.HTTP_200_OK)

            except Exception as e:
                logger.exception("Failed to send email.")
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

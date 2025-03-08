from rest_framework import serializers

class EmailSendSerializer(serializers.Serializer):
    to_address = serializers.EmailField()
    from_address = serializers.EmailField()
    from_name = serializers.CharField(required=False, allow_blank=True)
    reply_to_address = serializers.EmailField(required=False, allow_blank=True)
    cc_address = serializers.EmailField(required=False, allow_blank=True)
    subject = serializers.CharField(required=False, allow_blank=True)
    html_body = serializers.CharField(required=False, allow_blank=True)  # Now optional
    template_name = serializers.CharField(required=False, allow_blank=True)  # Added template_name
    context = serializers.DictField(required=False)

    def validate(self, data):
        """ Custom validation to ensure at least one of `html_body` or `template_name` is provided. """
        html_body = data.get("html_body", "").strip()
        template_name = data.get("template_name", "").strip()

        if not html_body and not template_name:
            raise serializers.ValidationError("Either `html_body` or `template_name` must be provided.")

        return data

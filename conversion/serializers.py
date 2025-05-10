from rest_framework import serializers

class ConversionInputSerializer(serializers.Serializer):
    """
    Main input serializer used for request validation.
    Requires all fields explicitly to ensure completeness.
    """
    from_currency = serializers.CharField()
    to_currency = serializers.CharField()
    amount = serializers.FloatField()


class ConversionInputExampleSerializer(serializers.Serializer):
    """
    Example serializer used only for Swagger UI documentation.
    Adds default values for a better interactive experience.
    """
    from_currency = serializers.CharField(default="CLP", help_text="Source fiat currency (e.g. CLP)")
    to_currency = serializers.CharField(default="PEN", help_text="Target fiat currency (e.g. PEN)")
    amount = serializers.FloatField(default=10000, help_text="Amount to convert")


class ConversionOutputSerializer(serializers.Serializer):
    """
    Output serializer for currency conversion result.
    Returns the converted amount and the intermediary cryptocurrency used.
    """
    converted_amount = serializers.FloatField()
    intermediate_currency = serializers.CharField()

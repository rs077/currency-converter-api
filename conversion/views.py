from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from drf_yasg.utils import swagger_auto_schema
from .services import get_best_conversion
from .serializers import ConversionInputSerializer, ConversionInputExampleSerializer, ConversionOutputSerializer


class ConvertCurrencyView(APIView):
    """
    API endpoint for converting one fiat currency to another using the best available
    intermediary cryptocurrency based on market data from Buda.com.
    """

    @swagger_auto_schema(
        request_body=ConversionInputExampleSerializer,  # Used only for Swagger docs
        responses={
            200: ConversionOutputSerializer,
            400: "Missing or invalid parameters",
            404: "No conversion path found"
        },
    )
    def post(self, request):
        """
        Converts a specified amount from one fiat currency to another using the best available
        intermediary cryptocurrency.

        Expects a JSON payload with:
        - from_currency: ISO code of the source fiat currency (e.g., CLP)
        - to_currency: ISO code of the target fiat currency (e.g., PEN)
        - amount: numeric value representing the amount to convert

        Returns the converted amount and the intermediary crypto used for the conversion.
        """
        serializer = ConversionInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        from_currency = serializer.validated_data['from_currency']
        to_currency = serializer.validated_data['to_currency']
        amount = serializer.validated_data['amount']

        result = get_best_conversion(from_currency, to_currency, amount)

        if result is None:
            return Response({"error": "No conversion path found"}, status=HTTP_404_NOT_FOUND)

        return Response(result, status=HTTP_200_OK)

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch

MOCK_MARKETS_RESPONSE = {
    "markets": [
        {"id": "btc-clp"},
        {"id": "btc-cop"},
        {"id": "btc-pen"},
    ]
}

MOCK_TICKERS = {
    "btc-clp": {"ticker": {"last_price": ["10000000.0"]}},
    "btc-cop": {"ticker": {"last_price": ["120000000.0"]}},
    "btc-pen": {"ticker": {"last_price": ["30000.0"]}},
}


def mock_get(url, *args, **kwargs):
    if "markets" in url and "ticker" not in url:
        class MockResp:
            def raise_for_status(self): pass
            def json(self): return MOCK_MARKETS_RESPONSE
        return MockResp()

    for market_id, data in MOCK_TICKERS.items():
        if market_id in url:
            class MockResp:
                def raise_for_status(self): pass
                def json(self): return data
            return MockResp()

    raise Exception("Invalid market id")


class ConvertCurrencyTests(APITestCase):
    @patch('requests.get', side_effect=mock_get)
    def test_successful_conversion(self, _):
        """Should return 200 with conversion result using BTC as intermediary."""
        response = self.client.post(reverse('convert'), {
            'from_currency': 'CLP',
            'to_currency': 'COP',
            'amount': 10000
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('converted_amount', response.data)
        self.assertIn('intermediate_currency', response.data)
        self.assertEqual(response.data['intermediate_currency'], 'BTC')

    @patch('requests.get', side_effect=mock_get)
    def test_all_currency_pairs(self, _):
        """Return 200 for all valid fiat currency combinations using BTC."""
        currencies = ['CLP', 'COP', 'PEN']
        for from_curr in currencies:
            for to_curr in currencies:
                if from_curr == to_curr:
                    continue
                response = self.client.post(reverse('convert'), {
                    'from_currency': from_curr,
                    'to_currency': to_curr,
                    'amount': 10000
                }, format='json')
                self.assertEqual(
                    response.status_code,
                    status.HTTP_200_OK,
                    msg=f"Failed for {from_curr} to {to_curr}"
                )
                self.assertIn('converted_amount', response.data)
                self.assertIn('intermediate_currency', response.data)

    def test_missing_fields(self):
        """Return 400 when required fields are missing."""
        response = self.client.post(reverse('convert'), {
            'from_currency': 'CLP',
            'amount': 10000
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('to_currency', response.data)

    def test_invalid_amount_type(self):
        """Return 400 when amount is not a valid number."""
        response = self.client.post(reverse('convert'), {
            'from_currency': 'CLP',
            'to_currency': 'COP',
            'amount': 'abc'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)

    @patch('requests.get', return_value=None)
    def test_no_conversion_path(self, _):
        """Return 404 if no conversion path is available."""
        response = self.client.post(reverse('convert'), {
            'from_currency': 'CLP',
            'to_currency': 'COP',
            'amount': 10000
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "No conversion path found"})

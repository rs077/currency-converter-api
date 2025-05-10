import requests
from typing import Optional, List, Dict

BASE_URL = "https://www.buda.com/api/v2/markets"
FIAT_CURRENCIES = {'CLP', 'COP', 'PEN'}


def fetch_last_price(market_id: str) -> Optional[float]:
    """
    Retrieves the price of the last transaction for the given market.
    """
    try:
        url = f"{BASE_URL}/{market_id}/ticker"
        resp = requests.get(url)
        resp.raise_for_status()
        return float(resp.json()['ticker']['last_price'][0])
    except Exception:
        return None


def get_available_intermediary_cryptos() -> List[str]:
    """
    Queries the active markets on Buda.com and returns a list of cryptocurrencies
    that are paired with at least two fiat currencies (CLP, COP, PEN).
    These are considered valid intermediaries for currency conversion.
    """
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        data = response.json()
    except Exception:
        return []

    pairs: Dict[str, set] = {}

    for market in data.get('markets', []):
        market_id = market['id']
        base, quote = market_id.upper().split('-')

        if base in FIAT_CURRENCIES and quote not in FIAT_CURRENCIES:
            pairs.setdefault(quote, set()).add(base)
        elif quote in FIAT_CURRENCIES and base not in FIAT_CURRENCIES:
            pairs.setdefault(base, set()).add(quote)

    return [crypto for crypto, fiats in pairs.items() if len(fiats) >= 2]


def get_best_conversion(from_currency: str, to_currency: str, amount: float) -> Optional[Dict[str, float | str]]:
    """
    Given a source currency, target currency, and amount, returns the best conversion result
    using a single intermediary cryptocurrency.
    """
    best_result: Optional[Dict[str, float | str]] = None
    cryptos = get_available_intermediary_cryptos()

    for crypto in cryptos:
        market1 = f"{crypto.lower()}-{from_currency.lower()}"
        market2 = f"{crypto.lower()}-{to_currency.lower()}"

        price_buy = fetch_last_price(market1)
        price_sell = fetch_last_price(market2)

        if price_buy and price_sell:
            crypto_amount = amount / price_buy
            final_amount = crypto_amount * price_sell

            if best_result is None or final_amount > best_result['converted_amount']:
                best_result = {
                    'converted_amount': round(final_amount, 2),
                    'intermediate_currency': crypto
                }

    return best_result

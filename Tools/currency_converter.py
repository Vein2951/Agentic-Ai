import requests

CURRENCY_URL = "https://api.frankfurter.app/latest"


def execute(arguments: dict):

    amount = arguments.get("amount")
    from_currency = arguments.get("from")
    to_currency = arguments.get("to")

    if amount is None:
        return "Currency Converter Error: 'amount' not provided."
    if not from_currency:
        return "Currency Converter Error: 'from' currency not provided."
    if not to_currency:
        return "Currency Converter Error: 'to' currency not provided."

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return "Currency Converter Error: 'amount' must be a number."

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    try:
        response = requests.get(
            CURRENCY_URL,
            params={
                "amount": amount,
                "from": from_currency,
                "to": to_currency,
            },
            timeout=10,
        )

        response.raise_for_status()
        data = response.json()

        rates = data.get("rates", {})
        converted = rates.get(to_currency)

        if converted is None:
            return f"Currency Converter Error: could not convert {from_currency} to {to_currency}."

        return (
            f"{amount} {from_currency} = {converted} {to_currency}"
        )

    except Exception as e:
        return f"Currency Converter Error: {e}"


if __name__ == "__main__":
    print("Currency converter tool\n")
    print(execute({"amount": 100, "from": "USD", "to": "INR"}))

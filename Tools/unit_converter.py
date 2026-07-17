# Conversion factors relative to a base unit for each category.
# length -> meters, weight -> kilograms, volume -> liters
UNIT_TABLE = {
    "length": {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "km": 1000.0,
        "in": 0.0254,
        "inch": 0.0254,
        "ft": 0.3048,
        "foot": 0.3048,
        "yd": 0.9144,
        "yard": 0.9144,
        "mi": 1609.344,
        "mile": 1609.344,
    },
    "weight": {
        "mg": 0.000001,
        "g": 0.001,
        "kg": 1.0,
        "lb": 0.453592,
        "lbs": 0.453592,
        "pound": 0.453592,
        "oz": 0.0283495,
        "ounce": 0.0283495,
        "ton": 1000.0,
    },
    "volume": {
        "ml": 0.001,
        "l": 1.0,
        "liter": 1.0,
        "gal": 3.78541,
        "gallon": 3.78541,
        "cup": 0.24,
        "tbsp": 0.0147868,
        "tsp": 0.00492892,
        "floz": 0.0295735,
    },
}

TEMPERATURE_UNITS = {"c", "celsius", "f", "fahrenheit", "k", "kelvin"}


def _find_category(unit: str):
    unit = unit.lower()
    for category, table in UNIT_TABLE.items():
        if unit in table:
            return category
    if unit in TEMPERATURE_UNITS:
        return "temperature"
    return None


def _convert_temperature(value: float, from_unit: str, to_unit: str):
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    # Normalize to Celsius first
    if from_unit in ("c", "celsius"):
        celsius = value
    elif from_unit in ("f", "fahrenheit"):
        celsius = (value - 32) * 5 / 9
    elif from_unit in ("k", "kelvin"):
        celsius = value - 273.15
    else:
        return None

    # Convert Celsius to the target unit
    if to_unit in ("c", "celsius"):
        return celsius
    elif to_unit in ("f", "fahrenheit"):
        return celsius * 9 / 5 + 32
    elif to_unit in ("k", "kelvin"):
        return celsius + 273.15

    return None


def execute(arguments: dict):

    value = arguments.get("value")
    from_unit = arguments.get("from_unit")
    to_unit = arguments.get("to_unit")

    if value is None:
        return "Unit Converter Error: 'value' not provided."
    if not from_unit:
        return "Unit Converter Error: 'from_unit' not provided."
    if not to_unit:
        return "Unit Converter Error: 'to_unit' not provided."

    try:
        value = float(value)
    except (TypeError, ValueError):
        return "Unit Converter Error: 'value' must be a number."

    from_category = _find_category(from_unit)
    to_category = _find_category(to_unit)

    if from_category is None:
        return f"Unit Converter Error: unknown unit '{from_unit}'."
    if to_category is None:
        return f"Unit Converter Error: unknown unit '{to_unit}'."
    if from_category != to_category:
        return (
            f"Unit Converter Error: cannot convert between "
            f"'{from_unit}' ({from_category}) and '{to_unit}' ({to_category})."
        )

    if from_category == "temperature":
        result = _convert_temperature(value, from_unit, to_unit)
        if result is None:
            return "Unit Converter Error: could not convert temperature."
        return f"{value} {from_unit} = {round(result, 4)} {to_unit}"

    table = UNIT_TABLE[from_category]
    base_value = value * table[from_unit.lower()]
    result = base_value / table[to_unit.lower()]

    return f"{value} {from_unit} = {round(result, 6)} {to_unit}"


if __name__ == "__main__":
    print("Unit converter tool\n")
    print(execute({"value": 10, "from_unit": "km", "to_unit": "mi"}))
    print(execute({"value": 100, "from_unit": "f", "to_unit": "c"}))
    print(execute({"value": 5, "from_unit": "kg", "to_unit": "lb"}))

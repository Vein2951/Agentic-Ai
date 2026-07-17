import os

# Load a local .env file if present (only matters for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def _get_secret(key: str):
    """Look for a secret first in environment variables, then in
    Streamlit's secrets manager (used automatically on Streamlit Cloud)."""
    value = os.getenv(key)
    if value:
        return value
    try:
        import streamlit as st
        return st.secrets[key]
    except Exception:
        return None


API_KEY = _get_secret("GROQ_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1"

MODEL_NAME = "llama-3.3-70b-versatile"


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

if not API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY not found. Set it as an environment variable, "
        "in a local .env file, or in Streamlit secrets."
    )

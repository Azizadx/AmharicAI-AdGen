import os
import sys
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class OPENAI_KEYS:
    def __init__(self):
        self.OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '') or None


class VECTORDB_KEYS:
    def __init__(self):
        self.VECTORDB_API_KEY = os.environ.get('WEAVIATE-API-KEY', '') or None
        self.VECTORDB_URL = os.environ.get('URL', '') or None
        self.VECTORDB_MODEL = os.environ.get('VECTORDB_MODEL', '') or None


def _get_openai_keys() -> OPENAI_KEYS:
    return OPENAI_KEYS()


def _get_vectordb_keys() -> VECTORDB_KEYS:
    return VECTORDB_KEYS()


def get_env_manager() -> dict:
    openai_keys = _get_openai_keys().__dict__
    vectordb_keys = _get_vectordb_keys().__dict__

    return {
        'openai_keys': openai_keys,
        'vectordb_keys': vectordb_keys,
    }

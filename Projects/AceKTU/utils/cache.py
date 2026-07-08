import json
import os

CACHE_FILE = "subject_cache.json"

def load_cache():
    """Load the cache file, or return empty dict if it doesn't exist yet."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def get_cached_result(subject_code):
    """Return cached search results for a subject code, or None if not cached."""
    cache = load_cache()
    return cache.get(subject_code)

def save_to_cache(subject_code, data):
    """Save/update search results for a subject code."""
    cache = load_cache()
    cache[subject_code] = data
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)
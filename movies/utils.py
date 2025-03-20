import requests
from django.conf import settings

def get_tmdb_data(endpoint, params=None):
    base_url = "https://api.themoviedb.org/3"
    image_base_url = "https://image.tmdb.org/t/p/w500"  # Adjust size if needed
    params = params or {}
    params['api_key'] = settings.TMDB_API_KEY
    response = requests.get(f"{base_url}/{endpoint}", params=params)
    data = response.json()
    
    # Add image base URL to each movie
    if 'results' in data:
        for movie in data['results']:
            if 'poster_path' in movie:
                movie['poster_url'] = f"{image_base_url}{movie['poster_path']}"
    return data
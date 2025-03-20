from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponse
import requests
from .models import Movie
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import get_user_model, login 


def get_tmdb_data(endpoint, params=None):
    api_key = "2b9de53ec25c391a3e158c7b026828a5"
    base_url = "https://api.themoviedb.org/3/"
    
    if params is None:
        params = {}
    params["api_key"] = api_key
    
    response = requests.get(base_url + endpoint, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code} - {response.text}")  # Debugging
        return None

@login_required
def profile(request):
    return render(request, 'movies/profile.html', {'profile': request.user})

class HomePageView(View):
    def get(self, request):
        popular_movies = get_tmdb_data('movie/popular', {'language': 'en-US', 'page': 1}) or {}
        movie_results = popular_movies.get('results', [])

        for movie in movie_results:
            movie['poster_url'] = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}"

        watchlist_movies = []
        favorite_movies = []

        watchlist_ids = request.session.get("watchlist", []) if request.user.is_authenticated else []
        favorite_ids = request.session.get("favorites", []) if request.user.is_authenticated else []

        for movie_id in watchlist_ids:
            movie = get_tmdb_data(f"movie/{movie_id}", {'language': 'en-US'})
            if movie:
                movie['poster_url'] = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}"
                watchlist_movies.append(movie)

        for movie_id in favorite_ids:
            movie = get_tmdb_data(f"movie/{movie_id}", {'language': 'en-US'})
            if movie:
                movie['poster_url'] = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}"
                favorite_movies.append(movie)

        return render(request, 'movies/home.html', {
            'movies': movie_results,
            'watchlist_movies': watchlist_movies,
            'favorite_movies': favorite_movies,
            'watchlist_ids': watchlist_ids,
            'favorite_ids': favorite_ids,
        })





class MovieDetailView(View):
    def get(self, request, movie_id):
        movie = get_tmdb_data(f"movie/{movie_id}", {'language': 'en-US'}) or {}
        recommendations = get_tmdb_data(f"movie/{movie_id}/recommendations", {'language': 'en-US'}) or {'results': []}

        if not movie:
            return HttpResponse("Movie details not available", status=500)

        # Ensure movie poster URL is included
        movie['poster_url'] = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}"

        for rec in recommendations['results']:
            rec['poster_url'] = f"https://image.tmdb.org/t/p/w200{rec.get('poster_path', '')}"

        return render(request, 'movies/detail.html', {
            'movie': movie,
            'recommendations': recommendations['results']
        })


@login_required
def toggle_watchlist(request, movie_id):
    if "watchlist" not in request.session:
        request.session["watchlist"] = []

    if movie_id in request.session["watchlist"]:
        request.session["watchlist"].remove(movie_id)
    else:
        request.session["watchlist"].append(movie_id)

    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', 'home'))  

@login_required
def toggle_favorites(request, movie_id):
    if "favorites" not in request.session:
        request.session["favorites"] = []

    if movie_id in request.session["favorites"]:
        request.session["favorites"].remove(movie_id)
    else:
        request.session["favorites"].append(movie_id)

    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', 'home'))  

@login_required
def watchlist_view(request):
    movie_ids = request.session.get("watchlist", [])
    movies = [get_tmdb_data(f"movie/{movie_id}") for movie_id in movie_ids]
    return render(request, 'movies/watchlist.html', {'movies': movies})

@login_required
def favorite_view(request):
    movie_ids = request.session.get("favorites", [])
    movies = [get_tmdb_data(f"movie/{movie_id}") for movie_id in movie_ids]
    return render(request, 'movies/favorites.html', {'movies': movies})


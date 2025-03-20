from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponse
import requests
from .models import Movie, Watchlist, FavoriteMovie
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
    movie_data = get_tmdb_data(f"movie/{movie_id}")  # Fetch movie details
    if not movie_data:
        return HttpResponse("Movie details not available", status=500)

    movie, created = Movie.objects.get_or_create(
        id=movie_data["id"],
        defaults={"title": movie_data["title"], "poster_path": movie_data.get("poster_path", "")}
    )

    watchlist_entry, created = Watchlist.objects.get_or_create(user=request.user, movie=movie)

    if not created:  # If already in watchlist, remove it
        watchlist_entry.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def toggle_favorites(request, movie_id):
    movie_data = get_tmdb_data(f"movie/{movie_id}")
    if not movie_data:
        return HttpResponse("Movie details not available", status=500)

    movie, created = Movie.objects.get_or_create(
        id=movie_data["id"],
        defaults={"title": movie_data["title"], "poster_path": movie_data.get("poster_path", "")}
    )

    favorite_entry, created = FavoriteMovie.objects.get_or_create(user=request.user, movie=movie)

    if not created:  # If already in favorites, remove it
        favorite_entry.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def watchlist_view(request):
    watchlist_entries = Watchlist.objects.filter(user=request.user)
    BASE_POSTER_URL = "https://image.tmdb.org/t/p/w500"

    watchlist_movies = [
        {
            'title': entry.movie.title,
            'poster_url': f"{BASE_POSTER_URL}{entry.movie.poster_path}" if entry.movie.poster_path else None,
            'id': entry.movie.id
        }
        for entry in watchlist_entries
    ]

    return render(request, 'movies/watchlist.html', {'movies': watchlist_movies})

@login_required
def favorite_view(request):
    favorite_entries = FavoriteMovie.objects.filter(user=request.user)
    BASE_POSTER_URL = "https://image.tmdb.org/t/p/w500"

    favorite_movies = [
        {
            'title': entry.movie.title,
            'poster_url': f"{BASE_POSTER_URL}{entry.movie.poster_path}" if entry.movie.poster_path else None,
            'id': entry.movie.id
        }
        for entry in favorite_entries
    ]

    return render(request, 'movies/favorites.html', {'movies': favorite_movies})

@login_required

def watchlist_favorites_view(request):
    watchlist_entries = Watchlist.objects.filter(user=request.user)
    favorite_entries = FavoriteMovie.objects.filter(user=request.user)

    BASE_POSTER_URL = "https://image.tmdb.org/t/p/w500"

    watchlist_movies = [
        {
            'title': entry.movie.title,
            'poster_url': f"{BASE_POSTER_URL}{entry.movie.poster_path}" if entry.movie.poster_path else None,
            'id': entry.movie.id
        }
        for entry in watchlist_entries
    ]

    favorite_movies = [
        {
            'title': entry.movie.title,
            'poster_url': f"{BASE_POSTER_URL}{entry.movie.poster_path}" if entry.movie.poster_path else None,
            'id': entry.movie.id
        }
        for entry in favorite_entries
    ]

    return render(request, "movies/mymovies.html", {
        'watchlist': watchlist_movies,
        'favorites': favorite_movies
    })

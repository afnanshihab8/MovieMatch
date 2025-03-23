from django.urls import path
from .views import HomePageView, MovieDetailView, toggle_watchlist, toggle_favorites, profile,  watchlist_view, favorite_view, watchlist_favorites_view , recommend_by_words

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('toggle_watchlist/<int:movie_id>/', toggle_watchlist, name='toggle_watchlist'),
    path('toggle_favorites/<int:movie_id>/', toggle_favorites, name='toggle_favorites'),
    path('', HomePageView.as_view(), name='home'),
    path('<int:movie_id>/', MovieDetailView.as_view(), name='movie_detail'),
    path('watchlist/', watchlist_view, name='watchlist'),
    path('favorites/', favorite_view, name='favorites'),
    path('my-movies/', watchlist_favorites_view, name='my_movies'),
    path("recommend-by-words/", recommend_by_words, name="recommend_by_words"),

]

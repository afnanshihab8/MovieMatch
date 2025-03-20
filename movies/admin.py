from django.contrib import admin
from .models import Profile, Watchlist, FavoriteMovie, Movie

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Movie)  
admin.site.register(Watchlist)
admin.site.register(FavoriteMovie)



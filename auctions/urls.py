from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newitem", views.add_item, name="add_item"),
    path('listing/<int:listing_id>', views.listing, name="listing"),
    path("close_bid/<int:listing_id>", views.close_bid, name="close_bid"),
    path("new_bid/<int:listing_id>", views.new_bid, name="new_bid"),
    path("add_watchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("watchlist", views.watchlist, name='watchlist'),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path('user_profile/<int:user_id>', views.user_profile, name="user_profile"),
    path('tags/<str:tag>', views.search_tag, name='search_tag'),
    path('search', views.search, name='search')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings/<str:type>", views.listings, name="listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addlisting", views.addlisting, name="addlisting"),
    path("addcategory", views.addcategory, name="addcategory"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("viewcategory", views.viewcategory, name="viewcategory")
]

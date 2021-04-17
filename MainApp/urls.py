from django.urls import path

from . import views

urlpatterns = [
        path("",views.index, name="index"),
        path("feed", views.feed, name="feed"),
        path("ngo/dashboard", views.ngo_dashboard, name="ngo_dashboard"),
        path("donor/dashboard", views.donor_dashboard, name="donor_dashboard"),
        path("volunteer/dashboard", views.volunteer_dashboard, name="volunteer_profile"),
]


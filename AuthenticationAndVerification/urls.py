from django.urls import path

from . import views

urlpatterns = [
    path('NGO/login', views.ngo_login, name="ngo_login"),
    path('donor/login', views.donor_login, name="donor_login"),
    path('volunteer/login', views.volunteer_login, name="volunteer_login"),
    path('NGO/register', views.ngo_register, name="ngo_register"),
    path('donor/register', views.donor_register, name="donor_register"),
    path('volunteer/register', views.volunteer_register, name="volunteer_register"),
    path('del', views.delete_session, name="del"),
    path('activate/<uname_b64>/<token>/', views.activate_email, name='activate'),
    path('reset_password/<uname_b64>/<user_type>/<token>',
        views.reset_password, name='reset_password'),
]

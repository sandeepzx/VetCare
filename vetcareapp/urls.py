from . import views
from django.urls import path

app_name = 'vetcareapp'

urlpatterns = [
    path("", views.home, name = 'home' ),
   
    path("contact/", views.contact, name = 'contact' ),
    path("services/", views.services, name = 'services' ),
    path("doctors/", views.doctors, name = 'doctors' ),
    path("doctors/doc/<str:username>/", views.doc, name = 'doc' ),
    path("con/<str:doctorname>/", views.consultation, name = 'consultations' ),
    path('check-date/', views.check_date, name='check_date'),
    path('message/<str:username>/<str:doctorname>/', views.chat, name='message'),
] 

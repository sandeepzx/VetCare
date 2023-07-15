from registration import views
from django.urls import path

app_name = 'registration'

urlpatterns = [
    path('register', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('doctor', views.doctor, name='doctor'),
    path('login_user',views.login_user, name='login_user'),
    path("book/<str:username>/<str:User_id>/", views.pet, name = 'book' ),
    path('pet_reg/', views.register, name='pet_reg'),
    path('doc_reg/',views.doctor,name='doc_reg'),
    path('logout/', views.logout, name='logout')
]

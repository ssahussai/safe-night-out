from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    #CRUD for drink session
    path('drinksessions/', views.drinksession_index, name='index'),
    path('drinksessions/<int:session_id>/', views.drinksession_detail, name='detail'),
    path('drinksessions/create/', views.DrinksessionCreate.as_view(), name='drinksessions_create'),
    path('drinksessions/<int:pk>/update/', views.DrinksessionUpdate.as_view(), name='drinksessions_update'),
    path('drinksessions/<int:pk>/delete/', views.DrinksessionDelete.as_view(), name='drinksessions_delete'),
]



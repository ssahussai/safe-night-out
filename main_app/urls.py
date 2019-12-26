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
    #CRUD for drinks
    # path('drinks/', views.DrinkList.as_view(), name='drinks_index'),
    # path('drinks/<int:pk>/', views.DrinkDetail.as_view(), name='drinks_detail'),
    path('drinks/create/', views.DrinkCreate.as_view(), name='drinks_create'),
    # should we keep drink edit view? potential problem if 
    # multiple people had same drink and getting different ABV/Effects
    path('drinks/<int:pk>/update/', views.DrinkUpdate.as_view(), name='drinks_update'),
    # should a user be able to delete a drink? it could be in another user's drinking session
    path('drinks/<int:pk>/delete/', views.DrinkDelete.as_view(), name='drinks_delete'),
    # Adding drinks to session
    # path('drinksession/<int:session_id>/add_drink/', views.add_drink_time, name='add_drink_time'),
]



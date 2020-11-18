from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('process', views.registration),
    path('process2', views.login),
    path('logout', views.logout),
    path('travel', views.travel),
    path('add_trip', views.add_travel), 
    path('submit_travel', views.submit_travel),	
    path('edit_travel/<int:travel_id>', views.edit_travel),  
    path('edit_submit/<int:travel_id>', views.edit_submit),
    path('delete_travel/<int:travel_id>', views.delete_travel),
    path('view/<int:travel_id>', views.view),
    path('join/<int:travel_id>', views.join),

]
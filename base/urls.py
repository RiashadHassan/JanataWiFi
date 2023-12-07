from django.urls import path
from base import views

urlpatterns = [
    path('', views.homePage, name='home' ),
    
    path('json_model/', views.jsonModel, name='json' ),
    
    path('save_json_to_database', views.save_json, name='save_json' ),
    path('sql_model/', views.display_sqlModel, name='sql' ),
    
    path('row/<str:pk>', views.Update_Delete.as_view(), name='update_delete'),
    
    path('charts/', views.line_chart, name='charts' ),

    
]  

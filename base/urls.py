from django.urls import path
from base import views

urlpatterns = [
    path('', views.homePage, name='home' ),
    
    path('save_json_to_database', views.save_json, name='save_json' ),
    
    path('json_model/', views.jsonModel, name='json' ),
    path('sql_model/', views.display_sqlModel, name='sql' ),
    
    path('row/<str:pk>', views.Update_Delete.as_view(), name='update_delete'),
    
    path('sql_model/charts/line_chart', views.line_chart, name='line_chart' ),
    path('sql_model/charts/bar_chart', views.bar_chart, name='bar_chart' ),
    path('sql_model/charts/multi_axis_chart', views.multi_axis_chart, name='multi_axis_chart' ),

    
]  

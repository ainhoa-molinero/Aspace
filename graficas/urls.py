from django.urls import path, include
from . import views

urlpatterns = [
    path('json_example/', views.json_example, name='json_example'),

    path('get_pie_graph/', views.get_pie_graph, name='get_pie_graph'),
    path('get_pie_graph/<str:id_usuario>', views.get_pie_graph, name='get_pie_graph'),

    path('get_time_graph/', views.get_time_graph, name='get_time_graph'),

    path('get_game_time_graph/', views.get_game_time_graph, name='get_game_time_graph'),
    path('get_game_time_graph/<str:id_usuario>', views.get_game_time_graph, name='get_game_time_graph'),

    path('get_user_results_time_graph/', views.get_user_results_time_graph, name='get_user_results_time_graph'),
    path('get_user_results_time_graph/<str:id_usuario>', views.get_user_results_time_graph, name='get_user_results_time_graph'),

    path('get_col_graph/', views.get_col_graph, name='get_col_graph'),
    path('get_col_graph/<str:id_usuario>', views.get_col_graph, name='get_col_graph'),
]

from django.http import HttpResponse
from django.urls import path
from . import views
from .views import create_team_request

urlpatterns = [
    path('list/', views.creator_list, name='creator_list'),  # Список создателей
    path('create/', views.create_creator, name='create_creator'),  # Создание создателя
    path('transfer-money/', views.transfer_money, name='transfer_money'),  # Перевод денег
    path('team-create/', views.create_team, name='create_team'),  # Создание команды
    path('team-list/', views.team_list, name='team_list'),  # Список команд
    path('delete-creator/<int:pk>/', views.delete_creator, name='delete_creator'),  # Удаление создателя
    path('delete-team/<int:team_id>/', views.delete_team, name='delete_team'),  # Удаление команды
    path('team-edit/<int:team_id>/', views.edit_team, name='team_edit'),  # Изменение команды
    path('creator-edit/<int:pk>/', views.edit_creator, name='creator_edit'),  # Изменение создателя
    path('members/create/', views.create_member, name='create_member'),
    path('member-list/', views.member_list, name='member_list'),
    #path('team/<int:team_id>/process_requests/', views.team_requests_view, name='team_requests'),
    path('create-team-request/', create_team_request, name='create_team_request'),
    path('success/', lambda request: HttpResponse("Request created successfully!"), name='success_page')

]

from django.urls import path
from .import views


urlpatterns = [
    path('', views.home, name='home' ),
    path('answer', views.answer, name='answer'),
]

urlpatterns += [
    path('equipment/', views.equipment_list, name='equipment_list'),
]

urlpatterns += [
    path('item_catalog/', views.item_catalog_list, name='item_catalog'),
]
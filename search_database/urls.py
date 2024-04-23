from django.urls import path, include
from search_database import views as search
from django.contrib import auth
from django.contrib.auth import views as auth_views
urlpatterns = [
      path('',search.search,name='view_file'),
      path('table/',search.table,name='view'),
      path('description/<str:pk>/',search.page,name='page'),

]
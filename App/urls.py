from django.urls import path
from App import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   path('',views.TaskList.as_view(),name='tasks'),
   path('task/<int:pk>/',views.TaskDetail.as_view(),name='task'),
   path('create-task/',views.TaskCreate.as_view(),name='task-create'),
   path('update-task/<int:pk>/',views.TaskUpdate.as_view(),name='task-update'),
   path('delete-task/<int:pk>/',views.TaskDelete.as_view(),name='task-delete'),
   path('login/',views.CustomLoginView.as_view(),name='login'),
   path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
   path('register/',views.Register.as_view(),name='register')
]

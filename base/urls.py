from django.urls import path
from .views import home, createtodo, completedtodo,currenttodos, viewtodo, completetodo,deletetodo, profile, ChangePasswordView, TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterView, TaskReorder 
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('',home,name='home'),
    path('profile/', profile, name='users-profile'),
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
    path('createtodo',createtodo,name='createtodo'),
    path('currenttodos', currenttodos,name='currenttodos'),
    path('createtodo',createtodo,name='createtodo'),
    path('completedtodo',completedtodo,name='completedtodos'),
    path('viewtodo/<int:todo_pk>',viewtodo,name='viewtodo'),
    path('viewtodo/<int:todo_pk>/complete',completetodo,name='completetodos'),
    path('viewtodo/<int:todo_pk>/delete',deletetodo,name='deletetodos'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
]

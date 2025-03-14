from django.urls import path
from events.views import manager_dashboard, user_dashboard,  create_task, view_task, update_task, delete_task,dashboard
# ,ViewProject

urlpatterns = [
    path('manager-dashboard/', manager_dashboard, name="manager-dashboard"),
    path('user-dashboard/', user_dashboard,name='user-dashboard'),
    # path('test/', Event),
    path('create-task/', create_task, name='create-task'),
    path('view_task/', view_task),
    # path('view_task/', ViewProject.as_view,name='view-task'),
    path('update-task/<int:id>/', update_task, name='update-task'),
    path('delete-task/<int:id>/', delete_task, name='delete-task'),
    path('dashboard', dashboard, name='dashboard')

]
from django.urls import path
from .views import AddTaskView, TaskListView,MarkTaskCompleteView,TaskCalendarView

urlpatterns = [
    path('tasks/add/', AddTaskView.as_view(), name='add-task'),
    path('tasks/', TaskListView.as_view(), name='list-tasks'),
    path('tasks/<int:task_id>/complete/', MarkTaskCompleteView.as_view(), name='complete-task'),
# path('tasks/export/csv/', ExportTasksCSV.as_view(), name='export-tasks'),
path('tasks/calendar/', TaskCalendarView.as_view(), name='calendar-view'),




]
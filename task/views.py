from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer

# class AddTaskView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             data = request.data.copy()
        
#             data['user'] = request.user.id
#             serializer = TaskSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({"success": True}, status=201)
#             return Response(serializer.errors, status=400)
#         except Exception as e:
#             import traceback
#             print("ERROR 🔥")
#             traceback.print_exc()
#             return Response({"error": str(e)}, status=500)

class AddTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)  # Set the user here
                return Response({"success": True}, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            import traceback
            print("ERROR 🔥")
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)

# class AddTaskView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             serializer = TaskSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(user=request.user)  # ✅ safer
#                 return Response({"success": True}, status=201)
#             return Response(serializer.errors, status=400)
#         except Exception as e:
#             import traceback
#             print("ERROR 🔥")
#             traceback.print_exc()
#             return Response({"error": str(e)}, status=500)



class TaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_tasks = Task.objects.filter(user=request.user).order_by('start_datetime')
        serializer = TaskSerializer(user_tasks, many=True)
        return Response(serializer.data)



from datetime import timedelta
from django.shortcuts import get_object_or_404


class MarkTaskCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.is_completed = True
        task.save()

        # Create next instance if recurring
        if task.is_recurring and task.repeat_type in ['Daily', 'Weekly']:
            delta = timedelta(days=1) if task.repeat_type == 'Daily' else timedelta(days=7)

            new_task = Task.objects.create(
                user=task.user,
                task_name=task.task_name,
                category=task.category,
                crop=task.crop,
                field=task.field,
                start_datetime=task.start_datetime + delta,
                end_datetime=task.end_datetime + delta if task.end_datetime else None,
                reminder=task.reminder,
                assigned_to=task.assigned_to,
                priority=task.priority,
                weather_sensitive=task.weather_sensitive,
                is_recurring=True,
                repeat_type=task.repeat_type,
                details=task.details,
            )

        return Response({"success": True, "message": "Task marked complete."})


from datetime import datetime, timedelta

class TaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        filter_type = request.GET.get('filter', 'all')

        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)

        tasks = Task.objects.filter(user=request.user)

        if filter_type == 'today':
            tasks = tasks.filter(start_datetime__date=today)
        elif filter_type == 'week':
            tasks = tasks.filter(start_datetime__date__range=(week_start, week_end))
        elif filter_type == 'month':
            tasks = tasks.filter(start_datetime__month=today.month)
        elif filter_type == 'completed':
            tasks = tasks.filter(is_completed=True)

        tasks = tasks.order_by('start_datetime')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskCalendarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get all tasks for the current month
        from calendar import monthrange
        today = datetime.now()
        start_of_month = today.replace(day=1)
        end_of_month = today.replace(day=monthrange(today.year, today.month)[1])

        tasks = Task.objects.filter(
            user=request.user,
            start_datetime__date__range=[start_of_month, end_of_month]
        ).order_by('start_datetime')

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)



class TaskSummaryView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(user=user)

        total_tasks = tasks.count()
        completed = tasks.filter(status='Completed').count()
        pending = tasks.filter(status='Pending').count()

        priority_count = {
            "High": tasks.filter(priority__iexact="High").count(),
            "Medium": tasks.filter(priority__iexact="Medium").count(),
            "Low": tasks.filter(priority__iexact="Low").count()
        }

        return Response({
            "total_tasks": total_tasks,
            "completed": completed,
            "pending": pending,
            "priority_breakdown": priority_count
        })



from rest_framework import status

class UpdateTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        serializer = TaskSerializer(task, data=request.data, partial=True)  # partial=True allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Task updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.delete()
        return Response({"success": True, "message": "Task deleted successfully."})

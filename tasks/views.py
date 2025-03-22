from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer
from django.shortcuts import render
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

def index(request):
    """
    Renders index page
    :param request:
    :return:
    """
    return render(request, 'tasks/index.html')

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['priority', 'completed', 'category', 'due_date']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Task.objects.filter(user=self.request.user)
        return Task.objects.none()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            raise PermissionDenied("You must be logged in to create a task.")

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'])
    def bulk_update(self, request):
        tasks_data = request.data
        updated_tasks = []
        for task_data in tasks_data:
            task = Task.objects.get(id=task_data['id'], user=request.user)
            serializer = TaskSerializer(task, data=task_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                updated_tasks.append(serializer.data)
        return Response(updated_tasks)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
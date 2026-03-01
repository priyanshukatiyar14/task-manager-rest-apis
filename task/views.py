from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsAdminOrOwner


class TaskPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                page_size = int(request.query_params.get(self.page_size_query_param, self.page_size))
                if page_size > self.max_page_size:
                    raise ValidationError({
                        'page_size': f'Page size cannot exceed {self.max_page_size}. Requested: {page_size}'
                    })
                if page_size <= 0:
                    raise ValidationError({
                        'page_size': 'Page size must be a positive integer.'
                    })
                return page_size
            except (ValueError, TypeError):
                raise ValidationError({
                    'page_size': 'Page size must be a valid integer.'
                })
        return self.page_size


class TaskListCreateView(generics.ListCreateAPIView):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    pagination_class = TaskPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["completed"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "updated_at", "completed"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return Task.objects.all()

        return Task.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    queryset = Task.objects.all()
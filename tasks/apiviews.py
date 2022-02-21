from tasks.models import Task, TaskHistory
from tasks.models import STATUS_CHOICES
from rest_framework.views import APIView
from rest_framework.response import Response
from tasks.serializers import TaskSerializer, TaskHistorySerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import (
    DjangoFilterBackend,
    FilterSet,
    CharFilter,
    ChoiceFilter,
    BooleanFilter,
    IsoDateTimeFilter,
)


class TaskFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")
    status = ChoiceFilter(choices=STATUS_CHOICES)
    completed = BooleanFilter()


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)

    def perform_create(self, serilaizer):
        serilaizer.save(user=self.request.user)


class TaskHistoryFilter(FilterSet):
    new_status = ChoiceFilter(choices=STATUS_CHOICES)
    updation_date = IsoDateTimeFilter()


class TaskHistoryAllViewSet(ListAPIView):
    queryset = TaskHistory.objects.all()
    serializer_class = TaskHistorySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskHistoryFilter

    def get_queryset(self):
        id = self.kwargs["pk"]
        if Task.objects.filter(id=id, user=self.request.user, deleted=False).exists():
            return TaskHistory.objects.filter(task_id=id)
        return TaskHistory.objects.none()


class TaskHistoryViewSet(ListAPIView):
    queryset = TaskHistory.objects.all()
    serializer_class = TaskHistorySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskHistoryFilter

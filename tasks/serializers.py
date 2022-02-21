from django.contrib.auth.models import User
from tasks.models import Task, TaskHistory
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")


class TaskSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        exclude = ['id', 'deleted']


class TaskHistorySerializer(ModelSerializer):
    class Meta:
        model = TaskHistory
        exclude = ['id']

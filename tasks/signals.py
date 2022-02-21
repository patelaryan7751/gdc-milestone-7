from django.db.models.signals import pre_save
from django.dispatch import receiver
from tasks.models import Task, TaskHistory


@receiver(pre_save, sender=Task)
def taskhistory_Update(sender, instance, **kwargs):
    if instance.id is None:
        pass
    else:
        current = instance
        previous = Task.objects.get(id=instance.id)
        if previous.status != current.status:
            print("old task: ", previous.status)
            print("current:", current.status)
            TaskHistory.objects.create(
                task_id=instance, old_status=previous.status, new_status=current.status)

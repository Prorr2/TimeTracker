from django.forms import ModelForm, CharField
from .models import Task
class TaskForm(ModelForm):
    name = CharField(max_length=50)
    class Meta:
        model = Task
        fields = ["name"]
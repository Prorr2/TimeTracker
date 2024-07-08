from django.contrib import admin
from .models import Task, Record
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name","init","minutes", "user"]
class RecordAdmin(admin.ModelAdmin):
    fields = ["name","date","minutes", "user"]
# Register your models here.
admin.site.register(Task, TaskAdmin),
admin.site.register(Record, RecordAdmin)

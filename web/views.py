from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_django, logout
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from .forms import TaskForm
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Task, Record
import math
from django.db.models.functions import ExtractDay
# Create your views here.
def login(request):
   if request.POST:
      user = authenticate(request, username=request.POST.get("username"), password = request.POST.get("password"))
      if user.is_authenticated:
         login_django(request, user)
   if request.user.is_authenticated:
      return redirect("home")
   return render(request, "web/login.html")

class programTask(ListView):
   template_name = "web/programTask.html"
   model = Task
   context_object_name = "Tasks"
   def get_queryset(self) -> QuerySet[Any]:
      name = ""
      if self.request.POST.get("name"):
         name = self.request.POST.get("name")
      return super().get_queryset().filter(user = self.request.user, name__contains = name)
   def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class home(ListView):
   template_name = "web/home.html"
   model = Task
   context_object_name = "Tasks"
   def get_queryset(self) -> QuerySet[Any]:
      return super().get_queryset().filter(user = self.request.user)

@require_POST
def post_task(request):
   form = TaskForm(data=request.POST)
   if form.is_valid():
      Task.objects.create(name=form.cleaned_data.get("name"), user = request.user)
   return redirect("home")

@require_POST
def post_action(request):
   id = request.POST.get("id")
   task = Task.objects.get(pk = id)
   if request.POST.get("action") != "Reset":
        if not task.real_init:
           task.real_init = timezone.now()
        if task.init:
            difference = timezone.now() - task.init
            task.minutes += math.floor(difference.total_seconds() / 60)
            task.init = None
            task.user = request.user
            Record.objects.create(name = task.name, minutes = math.floor(difference.total_seconds() / 60), date = datetime.now(), user = request.user)
            task.save()
        else:
            task.init = timezone.now()
            task.user = request.user
            task.save()
   else:
      task.minutes = 0
      task.real_init = None
      task.init = None
      task.user = request.user
      task.save()
   return redirect("home")
def schedule_redirect(request, index):
      if request.POST:
         id = request.POST.get("id")
         obj = Record.objects.get(id = id)
         obj.delete()
      records_by_day = []
      firesubjects = {}
      Tasks = Task.objects.filter(user = request.user)
      first = Record.objects.filter(user = request.user).order_by(ExtractDay('date')).first()
      print(first.date)
      for i in range(7):
         records_by_day.append([])
      for record in Record.objects.filter(date__gte = datetime.now() - timedelta(days=7 * index), date__lte = datetime.now() - timedelta(days=7 * (index - 1)), user = request.user).order_by(ExtractDay('date')):
        day = record.date.weekday()
        if not records_by_day[day]:
            records_by_day[day] = []
        if record.minutes > 50:
           firesubjects[record.date] = record.name
        records_by_day[day].append(record)
      print(records_by_day)
      Records = reversed(records_by_day)
      Fire = firesubjects
      if index > 0:
         index_less = index -1
      index_more = index +1
      return render(request, "web/schedule.html", {"Tasks" : Tasks, "Records" : Records, "Fire" : Fire, "index_less" : index_less, "index_more": index_more})

@require_POST
def post_program(request):
   date = request.POST.get("date")
   hours = request.POST.get("hours")
   time = request.POST.get("time")
   id = request.POST.get("selected")
   task = Task.objects.get(id = id)
   if date and hours and id:
      minutes = int(hours[hours.find(":") + 1 : len(hours)])
      hours = int(hours[0 : hours.find(":")])
      totalMinutes = (hours * 60) + minutes
      dateStr = f"{date} {time}"
      dateObj = datetime.strptime(dateStr, "%Y-%m-%d %H:%M")

      task.init = dateObj
      task.minutes = totalMinutes
      Record.objects.create(name = task.name, minutes = totalMinutes, date = dateObj, user = request.user)
      task.minutes += totalMinutes
      task.save()
      return redirect("schedule_redirect", 1)


def off(request):
   logout(request)
   return redirect('login')
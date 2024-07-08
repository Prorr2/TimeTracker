from django.urls import include, path
from .views import login, home, post_task, post_action, schedule_redirect,off, programTask, post_program
urlpatterns = [
    path("", login, name='login'),
    path("home/", home.as_view(), name='home'),
    path("schedule/<int:index>", schedule_redirect, name='schedule_redirect'),
    path("endpoint/new-task", post_task, name='post_task'),
    path("endpoint/action", post_action, name='post_action'),
    path("endpoint/ProgramTaskAction", post_program, name='post_program'),
    path("off",off,name="off"),
    path("taskByDay", programTask.as_view(), name="programTask")
]
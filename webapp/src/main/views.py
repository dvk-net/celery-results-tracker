from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from celery.result import AsyncResult
from rest_framework import authentication, permissions
# Create your views here.
from . import tasks

def home(request):
    tasks.download_a_cat.delay()
    return HttpResponse('<h1>Гружу кота!!!!</h1>')


class TaskSetter(APIView):
    # authentication_classes = [authentication.]
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        res = tasks.cpu_task.delay()
        return Response(res.id)

class TaskGetter(APIView):
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        task_id = request.GET.get('task_id')
        if task_id:
            res = AsyncResult(task_id)
            return Response(res.state)
        return Response("no id provided")
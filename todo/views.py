from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from todo.models import Todo
from django.http import HttpResponseRedirect
import requests

# Create your views here.

def index(request):
    response = requests.get("http://api.ipstack.com/149.140.187.82?access_key=2f8b706956c38ab53738b8c285cb73f4&format=1")
    geodata = response.json()

    todo_items = Todo.objects.all().order_by("-added_date")
    return render(request, "main/index.html", {
        "todo_items" : todo_items,
 
        "ip" : geodata["ip"],
        "city": geodata["city"],
    })

@csrf_exempt
def add_todo(request):
    current_date = timezone.now()
    content = request.POST["content"]
    created_obj = Todo.objects.create(added_date = current_date, text = content)
    length_of_todos = Todo.objects.all().count()
    return HttpResponseRedirect("/")

@csrf_exempt
def delete_todo(request, todo_id):
    Todo.objects.get(id = todo_id).delete()
    print(todo_id)
    return HttpResponseRedirect("/")
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList

# def say_hello(request):
#     #return HttpResponse("Hello World RL")
#     x = 1
#     y = 2
#     a = {"name": "RL"}
#     return render(request, "hello.html", a)

def index(response, id):
    ls = ToDoList.objects.get(id=id)
    return render(response, "playground/list.html", {"ls": ls})

def home(response):
    return render(response, "playground/home.html", {"name": "test"})

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
        return HttpResponseRedirect("/%i" %t.id)

    else:
        form = CreateNewList()
    return render(response, "playground/create.html", {"form":form})

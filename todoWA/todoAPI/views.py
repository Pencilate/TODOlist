from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,JsonResponse,HttpResponseNotFound
from django.contrib.auth.models import User
from todoAPI.models import Todo
from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
import json
import logging
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
def loginView(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
        except MultiValueDictKeyError:
            return JsonResponse({"message":"Ensure the request contains both 'username' and 'password' field"},status=400)
        if not username or not password:
            return JsonResponse({"message":"Ensure the 'username' and/or 'password' field in the data are not blank"},status=400)

        print("Username is "+username)
        print("Password is "+password)
        user = authenticate(request, username=username,password=password)
        if user is not None:
            print("User Authenticated")
            login(request,user)
            return JsonResponse(data={"userId":user.id})
        else:
            print("User Invalid")
            return JsonResponse({"message":"You have entered invalid credential"}, status=401)
    else:
        return JsonResponse({"message":"Please use POST request header"}, status=405)

def logoutView(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse(data={"message":"Successful logout"})
        else:
            return JsonResponse({"message":"Unauthorized Action. You are not logged in"}, status=401)
    else:
        return JsonResponse({"message":"Please use POST REST API to login"}, status=405)   

class TodoController(View):  
    http_method_names = ['get','post','put','delete']

    def post(self,request,**kwargs):

        if(str(request.body) == "b''"):
            return JsonResponse({"message":"Wrong REST API Method used. Your request body appear to be empty but this is a POST endpoint."}, status=405)    
        if request.user.is_authenticated:
            if len(kwargs) == 0:
                try:
                    title = request.POST['title']
                    description = request.POST['description']
                except MultiValueDictKeyError:
                    return JsonResponse({"message":"Bad Request. Ensure the data contains both 'title' and 'description' field"}, status=400)


                if not title or not description:
                    return JsonResponse({"message":"Bad Request. Ensure the data you sent are proper"}, status=400)
                    
                todo = Todo(title=title,description=description,status=False,createdBy_id=request.user.id)
                todo.save()
                oneTodoData = list(Todo.objects.filter(id=todo.id).values())[0]
                del oneTodoData["createdBy_id"]
                return JsonResponse(oneTodoData, status=201)

            else:
                return JsonResponse({"message":"Wrong REST API Method used. Are you trying to update a TODO?."}, status=405)    
        else:
            return JsonResponse({"message":"You are not logged in"}, status=401)




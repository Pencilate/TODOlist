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

# Create your views here.
def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print("Username is "+username)
        print("Password is "+password)
        user = authenticate(request, username=username,password=password)
        if user is not None:
            print("User Authenticated")
            login(request,user)
            return JsonResponse(data={"userId":user.id})
        else:
            print("User Invalid")
            return HttpResponse(json.dumps({"message":"You have entered invalid credential"}), content_type='application/json', status=401)
    else:
        return HttpResponse(json.dumps({"message":"Please use POST request header"}), content_type='application/json', status=405)

def logoutView(request):
    if request.method == 'POST':
        if request.user.is_authenticated == True:
            logout(request)
            return JsonResponse(data={"message":"Successful logout"})
        else:
            return HttpResponse(json.dumps({"message":"Unauthorized Action. You are not logged in"}), content_type='application/json', status=401)
    else:
        return HttpResponse(json.dumps({"message":"Please use POST REST API to login"}), content_type='application/json', status=405)    

class TodoController(View):  
    http_method_names = ['get','post','put','delete']

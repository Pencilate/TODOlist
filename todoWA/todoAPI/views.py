from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,JsonResponse,HttpResponseNotFound
from django.contrib.auth.models import User
from todoAPI.models import Todo
from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views import View
import json
import logging
from django.utils.datastructures import MultiValueDictKeyError
from django.forms.models import model_to_dict

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
    http_method_names = ['get','post']

    def get(self,request):
        if request.user.is_authenticated:
                data = list(Todo.objects.filter(createdBy_id = request.user.id).values('id','title','description','status'))
                return JsonResponse({"records": data})
        else:
            return JsonResponse({"message":"Unauthorized Access. You need to login to access this TODO."}, status=401)
          
    def post(self,request):
        if request.user.is_authenticated:
            try:
                title = request.POST['title']
                description = request.POST['description']
            except MultiValueDictKeyError:
                return JsonResponse({"message":"Bad Request. Ensure the data contains 'title' and 'description' field."}, status=400)

            if not title or not description:
                return JsonResponse({"message":"Bad Request. Ensure the data you sent do not have blank values."}, status=400)
                
            todo = Todo(title=title,description=description,status=False,createdBy_id=request.user.id)
            todo.save()
            return JsonResponse({"id":todo.id,"title":todo.title,"description":todo.description,"status":todo.status},status=201)
        else:
            return JsonResponse({"message":"Unauthorized Access. You need to login to create this TODO."}, status=401)

class TodoControllerSpecific(View):
    http_method_names = ['get','put','delete']

    def get(self,request,**kwargs):
        # logger = logging.getLogger()
        # logger.debug("Number of arguments sent to GET: "+str(len(kwargs)))
        if request.user.is_authenticated:
            try:
                data = Todo.objects.get(id=kwargs["todoid"])
            except ObjectDoesNotExist:
                return JsonResponse({"message":"Not Found. This TODO you are trying to access does not exist."}, status=404)
            except MultipleObjectsReturned:
                return JsonResponse({"message":"Internal Server Error. A problem has occured retrieveing your TODO"}, status=500)
            
            if data.createdBy_id == request.user.id:
                return JsonResponse({"id":data.id,"title":data.title,"description":data.description,"status":data.status})
            else:
                return JsonResponse({"message":"Forbidden Resource. You are not authorized to access this TODO."}, status=403)
        else:
            return JsonResponse({"message":"Unauthorized Access. You need to login to access this TODO."}, status=401)

    def put(self,request, **kwargs):
        if request.user.is_authenticated:
            request.method = 'POST'
            try:
                title = request.POST['title']
                description = request.POST['description']
                status = request.POST['status']
            except MultiValueDictKeyError:
                return JsonResponse({"message":"Bad Request. Ensure the data contains 'title', 'description' and 'status' field"}, status=400)

            if not title or not description or not status:
                return JsonResponse({"message":"Bad Request. Ensure the data you sent do not have blank values"}, status=400)
            
            try:
                todo = Todo.objects.get(id=kwargs["todoid"])
            except ObjectDoesNotExist:
                return JsonResponse({"message":"Not Found. This TODO you are trying to update does not exist"},status=404) 
            
            if(todo.createdBy_id == request.user.id):
                todo.title = title
                todo.description = description
                todo.status = status
                todo.save()
                
                return JsonResponse({"id":todo.id,"title":todo.title,"description":todo.description,"status":todo.status}, status=200)
            else:
                return JsonResponse({"message":"Forbidden Resource. You are not authorised to update this TODO"},status=403)
        else:
            return JsonResponse({"message":"Unauthorized Access. You need to login to update this todo"}, status=401)
          
    def delete(self,request,**kwargs):
        if request.user.is_authenticated:
            try:
                todo = Todo.objects.get(id=kwargs["todoid"])
            except ObjectDoesNotExist:
                return JsonResponse({"message":"Not Found. This TODO you are trying to delete does not exist"},status=404) 
            
            if(todo.createdBy_id == request.user.id):
                count = todo.delete()
                return JsonResponse({"message": "Successfully Deletion"})
            else:
                return JsonResponse({"message":"Forbidden Resource. You are not authorized to delete this TODO."}, status=403)
        else:
            return JsonResponse({"message":"Unauthorized Access. You need to login to delete this TODO."}, status=401)


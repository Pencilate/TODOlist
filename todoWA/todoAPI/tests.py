from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from todoAPI.models import Todo
from urllib.parse import urlencode

# Create your tests here.
class UserTests(TestCase):
    # @classmethod
    def setUp(self):
        testuser = User.objects.create_user(username="Johnny",password="12345678")
    
    def test_loginTestWrongInfo(self):
        c = Client()
        response = c.post('/todoapi/login/',{'username':'John','password':'1234568'})
        self.assertEqual(response.status_code,401)

    def test_loginTestCorrectInfo(self):
        c = Client()
        response = c.post('/todoapi/login/',{'username':'Johnny','password':'12345678'})
        self.assertEqual(response.status_code,200)

    def test_logoutTest(self):
        
        c = Client()
        c.login(username="Johnny",password="12345678")
        response = c.post('/todoapi/logout/')
        self.assertEqual(response.status_code,200)
        #After logging out
        response = c.post('/todoapi/logout/')
        self.assertEqual(response.status_code,401)
     
class TodoTests(TestCase):

    def test_getTodo(self):
        Todo.objects.all().delete()
        User.objects.all().delete()
        testuser = User.objects.create_user(username="JohnnyTodo",password="12345678")
        todo = Todo.objects.create(title="TestTodoGET",description="Test TODO Description",status=False,createdBy_id=1)
        todo2 = Todo.objects.create(title="TestTodoGET2",description="Test TODO2 Description",status=False,createdBy_id=1)
        todo.save()
        todo2.save()

        c = Client()
        c.login(username="JohnnyTodo",password="12345678")
        response = c.get('/todoapi/todos/')
        self.assertEqual(response.status_code,200)

        c.logout() 
        response = c.get('/todoapi/todos/')
        self.assertEqual(response.status_code,401)




    def test_getSpecificTodo(self):
        Todo.objects.all().delete()
        User.objects.all().delete()
        testuser = User.objects.create_user(username="JohnnyTodoGET",password="12345678")
        todo = Todo.objects.create(title="TestTodoGET",description="Test TODO Description",status=False,createdBy_id=1)
        todo.save()

        c = Client()
        c.login(username="JohnnyTodoGET",password="12345678")
        response = c.get('/todoapi/todos/'+str(todo.id))
        print(response.context)
        self.assertEqual(response.status_code,200)

    def test_getSpecificTodo(self):
        Todo.objects.all().delete()
        User.objects.all().delete()
        testuser = User.objects.create_user(username="JohnnyTodo",password="12345678")
        testuser2 = User.objects.create_user(username="JannyTodo",password="12345678")

        todo = Todo.objects.create(title="TestTodo",description="Test TODO Description",status=False,createdBy_id=testuser.id)
        todoAlt = Todo.objects.create(title="TestTodoAlt",description="Test TODO belong to another user",status=False,createdBy_id=testuser2.id)
        todo.save()
        todoAlt.save()

        c = Client()
        c.login(username="JohnnyTodo",password="12345678")
        response = c.get('/todoapi/todos/'+str(todo.id))
        print(response.context)
        self.assertEqual(response.status_code,200)

        response = c.get('/todoapi/todos/10000')
        self.assertEqual(response.status_code,404)

        response = c.get('/todoapi/todos/'+str(todoAlt.id))
        self.assertEqual(response.status_code,403)

        c.logout()
        response = c.get('/todoapi/todos/'+str(todo.id))
        self.assertEqual(response.status_code,401)

    def test_postTodo(self):
        Todo.objects.all().delete()
        User.objects.all().delete()
        testuser = User.objects.create_user(username="JohnnyTodo",password="12345678")

        c = Client()
        c.login(username="JohnnyTodo",password="12345678")

        response = c.post('/todoapi/todos/',{"title":"Todo from POST", "description":"POST Todo Description" })
        self.assertEqual(response.status_code,201)

        response = c.post('/todoapi/todos/',{"title":"", "description":"POST Todo Description" })
        self.assertEqual(response.status_code,400)

        response = c.post('/todoapi/todos/',{"description":"POST Todo Description" })
        self.assertEqual(response.status_code,400)

        c.logout()
        response = c.post('/todoapi/todos/',{"title":"Todo from POST", "description":"POST Todo Description" })
        self.assertEqual(response.status_code,401)

    def test_putTodo(self):
        Todo.objects.all().delete()
        User.objects.all().delete()
        testuser = User.objects.create_user(username="JohnnyTodo",password="12345678")
        testuser2 = User.objects.create_user(username="JannyTodo",password="12345678")
        todo = Todo.objects.create(title="TestTodo",description="Test TODO Description",status=False,createdBy_id=testuser.id)
        todoAlt = Todo.objects.create(title="TestTodoAlt",description="Test TODO belong to another user",status=False,createdBy_id=testuser2.id)
        todo.save()
        todoAlt.save()

        c = Client()
        c.login(username="JohnnyTodo",password="12345678")
        
        #https://github.com/jgorset/django-respite/issues/38#issuecomment-7445003
        response = c.put('/todoapi/todos/'+str(todo.id),urlencode({ "title":"TostTodoPUT", "description":"Updated", "status":True}),content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code,200)
        
        response = c.put('/todoapi/todos/'+str(todo.id),urlencode({"title":"", "description":"Updated", "status":True}),content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code,400)

        response = c.put('/todoapi/todos/'+str(todo.id),urlencode({"description":"Updated", "status":True}),content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code,400)

        response = c.put('/todoapi/todos/10000',urlencode({"title":"TostTodoPUT", "description":"Updated", "status":True}),content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code,404)

        response = c.put('/todoapi/todos/'+str(todoAlt.id),urlencode({"title":"TostTodoPUT", "description":"Updated", "status":True}),content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code,403)

        c.logout()
        response = c.put('/todoapi/todos/'+str(todo.id),urlencode({"title":"TostTodoPUT", "description":"Updated", "status":True}),content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code,401)

    def test_deleteTodo(self):
        Todo.objects.all().delete()
        User.objects.all().delete()
        testuser = User.objects.create_user(username="JohnnyTodo",password="12345678")
        testuser2 = User.objects.create_user(username="JannyTodo",password="12345678")
        todo = Todo.objects.create(title="TestTodo",description="Test TODO Description",status=False,createdBy_id=testuser.id)
        todoAlt = Todo.objects.create(title="TestTodoAlt",description="Test TODO belong to another user",status=False,createdBy_id=testuser2.id)
        todo.save()
        todoAlt.save()

        c = Client()
        c.login(username="JohnnyTodo",password="12345678")

        response = c.delete('/todoapi/todos/'+str(todo.id))
        self.assertEqual(response.status_code,200)
        self.assertLess(len(Todo.objects.all()),2)

        response = c.delete('/todoapi/todos/'+str(todoAlt.id))
        self.assertEqual(response.status_code,403)

        c.logout()
        response = c.delete('/todoapi/todos/'+str(todo.id))
        self.assertEqual(response.status_code,401) 

        


        

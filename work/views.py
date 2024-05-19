from django.shortcuts import render,redirect
from django.views.generic import View
from work.forms import Register,Loginform,TaskForm
from work.models import User,Taskmodel
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator

#decorator
def signin_required(fn):
    def wrapper(request,**kwargs):
        if not request.user.is_authenticated:
           return redirect("login")
        else:
            return fn(request,**kwargs)
    return wrapper

def deletelogin_required(fn):
    def wrapper(request,**kwargs):
        id=kwargs.get("pk")
        obj=Taskmodel.objects.get(id=id)
        if obj.user!=request.user:
            return redirect("login")
        else:
            return fn(request,**kwargs)
    return wrapper
        



#registration
class Registration(View):

    def get(self,request,**kwargs):

        form=Register()

        return render(request,"register.html",{"form":form})
    
    def post(self,request,**kwargs):

        form=Register(request.POST)

        if form.is_valid():
        
            #form.save()
            User.objects.create_user(**form.cleaned_data)
            form=Register()

            return redirect("login")
        

        

class Signin(View):

    def get(self,request,**kwargs):

        form=Loginform()
        
        return render(request,"login.html",{"form":form})
    
    def post(self,request,**kwargs):

        form=Loginform(request.POST)

        if form.is_valid():
            print(form.cleaned_data)

            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")

            user_obj=authenticate(username=u_name,password=pwd)

            if user_obj:
                print("valid credentials")
                login(request,user_obj)
                return redirect("task")
            
            else:
                 form=Loginform
                 return render(request,"login.html",{"form":form})
            



#@method_decorator(decoratorname,name='dispatch')
@method_decorator(signin_required,name='dispatch')
class Add_task(View):
    def get(self,request,**kwargs):
        form=TaskForm()
        data=Taskmodel.objects.filter(user=request.user).order_by('completed')
        return render(request,"index.html",{"form":form,"data":data})
    
    def post(self,request,**kwargs):
        form=TaskForm(request.POST)
        if form.is_valid():
            #Taskmodel.objects.create(**form.cleaned_data)
            form.instance.user=request.user
            form.save()
            messages.success(request,"task added successfully")
            
            form=TaskForm()
            #READ
            #data=Taskmodel.objects.all().order_by('completed')
            data=Taskmodel.objects.filter(user=request.user).order_by('completed')


        return render(request,"index.html",{"form":form,"data":data})
    

    
#delete
@method_decorator(deletelogin_required,name='dispatch')
class Delete_task(View):
    def get(self,request,**kwargs):
        id=kwargs.get("pk")
        Taskmodel.objects.get(id=id).delete()
        return redirect("task")
    

#update
class Task_edit(View):
     def get(self,request,**kwargs):
         id=kwargs.get("pk")
         obj=Taskmodel.objects.get(id=id)
         print(obj)
         print(obj.completed)
         if obj.completed==False:
             obj.completed=True
             print(obj.completed)
             obj.save() #model form use cheythakondu obj.save kodukam
         return redirect("task")
 
#signout
class Signout(View):
 def get(self,request):
    logout(request)
    return redirect('login')


#delete account
class User_del(View):
    def get(self,request,**kwargs):
        id=kwargs.get("pk")
        User.objects.get(id=id).delete()
        return redirect("login")

#update_user
class Update_user(View):
    def get(self,request,**kwargs):
        id=kwargs.get("pk")
        data=User.objects.get("id=id")
        form=Register(instance=data)
        return render(request,"register.html",{"form":form})
    def post(self,request,**kwargs):
        id=kwargs.get("pk")
        data=User.objects.get(id=id)
        form=Register(request.Post,instance=data)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect("login")







# -*- coding: utf-8 -*-  
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from documents.views import getDoc

def returnTemp(request,name):
    return render_to_response(name)

def register(request):
    return render_to_response('register.html',{},context_instance=RequestContext(request))

def user_register_checker(request):
    #=========== fetch post date ==========# 
    post_username = request.POST["username"]
    post_password = request.POST["password"]
    post_email = request.POST["email"]
    succ = (len(User.objects.all().filter(username=post_username))==0)
    if succ:
        user = User.objects.create_user(username = post_username, password = post_password, email = post_email)
        user.save()
        return HttpResponse("success /")
    else:
        return HttpResponse("fail unavailable username")

def login(request):
    user = request.user
    if user.is_authenticated() :
        if user.is_staff:
            return HttpResponseRedirect('/admin/')
        else:
            return HttpResponseRedirect('/homepage/')
    else:
        return render_to_response('login.html',{},context_instance=RequestContext(request))

def user_login_checker(request):
    print "user_login_checker receive"
    #=========== fetch post date ==========# 
    post_username = request.POST["username"]
    post_password = request.POST["password"]
    post_admin = (request.POST["admin"]=="checked")
    #=========== login logic ==========# 
    user = auth.authenticate(username = post_username, password = post_password)
    if user is None:
        return HttpResponse("fail 用户名或密码错误")
    if post_admin:
        if user.is_staff:
            auth.login(request, user)
            return HttpResponse("success /admin/")
        else:
            return HttpResponse("fail 该用户不是管理员")
    else:
        if user.is_staff:
            return HttpResponse("fail 该用户是管理员,不能作为普通用户登录")
        else:
            auth.login(request, user)
            return HttpResponse("success /homepage/")

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
    
def homepage(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    user = request.user
    try: cUser = User.objects.all().filter(username=request.POST["current_username"])
    except: cUser = user
    httpdict = {}
    httpdict["login_user"] = user
    httpdict["current_user"] = cUser
    httpdict["current_userbooks"] = getDoc(cUser)
    return render_to_response('userpage.html',httpdict,context_instance=RequestContext(request))
    
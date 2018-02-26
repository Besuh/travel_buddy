# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from models import User, Trip
import bcrypt
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, "travelBuddy/index.html")
def register(request):
    regis = User.objects.registration(request.POST)
    if regis[0]:
        request.session["user_id"]= regis[1].id
        messages.add_message(request, messages.SUCCESS, "you've  successfully registered")
        return redirect("/travels")
    else:
        for error in regis[1]:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/main")
def login(request):
    log = User.objects.login(request.POST)
    if log["is_valid"]:
        request.session["user_id"]= log["user"].id
        messages.add_message(request, messages.SUCCESS, "You've logged in")
        return redirect("/travels")
    else:
        for error in log["errors"]:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/main")
def logout(request):
    request.session.clear()
    messages.add_message(request, messages.SUCCESS, "You have just logged out, goodbye!")
    return redirect("/main")
def travels(request):
    user = User.objects.get(id=request.session["user_id"])
    data = {
        "user": user,
        "yours": Trip.objects.filter(creator= request.session["user_id"]),
        "joined": Trip.objects.filter(joiners = request.session["user_id"]),
        "plans": Trip.objects.all(),

    }
    return render(request, "travelBuddy/travels.html", data)
def destination(request, number):
    data = {
        "trip": Trip.objects.filter(id=number),
        "joiners": User.objects.filter(joining=number),
    }
    return render(request, "travelBuddy/destination.html", data)
def add(request):
    return render(request, "travelBuddy/add.html")
def new(request):
    newPlan = Trip.objects.tripValidation(request.POST, request.session["user_id"])
    if newPlan[0]:
        messages.add_message(request, messages.SUCCESS, "You've made a new plan!")
        return redirect("/travels")
    else:
        for error in newPlan[1]:
            messages.add_message(request, messages.ERROR, error)
            return redirect("/travels/add")
def join(request, id):
    newJoin = Trip.objects.join(id, request.session["user_id"])
    if "error" in newJoin:
        messages.add_message(request, messages.ERROR, newJoin["error"])
        return redirect("/travels")
    else:
        messages.add_message(request, messages.SUCCESS, "You've joined the the plan!")
        return redirect("/travels")
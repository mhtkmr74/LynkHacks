from django.shortcuts import render
import json
from .models import Victims
from django.http import HttpResponse

# Create your views here.


def signup(request):
    received_json_data = json.loads(request.body)
    name = received_json_data['name']
    number = received_json_data['mobile_number']
    location = received_json_data['location']
    print("Issue possible in location")
    victim_obj = Victims()
    victim_obj.name = name
    victim_obj.number = number
    victim_obj.location = location
    victim_obj.save()
    print("Issue can be here in primary key victim", victim_obj.pk)
    return HttpResponse(json.dumps({"victim_id": victim_obj.pk}), content_type="application/json")


def login(request):
    number = request.GET['mobile_number']
    victim_data_obj = Victims.objects.filter(number=number)
    result = victim_data_obj[0]
    return HttpResponse(status=200)

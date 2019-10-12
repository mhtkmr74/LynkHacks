from django.shortcuts import render
import json
from .models import Volunteers
from django.http import HttpResponse

# Create your views here.


def signup(request):
    received_json_data = json.loads(request.body)
    print("Issue possible in location")
    volunt_obj = Volunteers()
    volunt_obj.name = received_json_data['name']
    volunt_obj.number = received_json_data['mobile_number']
    volunt_obj.location = received_json_data['location']
    volunt_obj.password = received_json_data['password']
    volunt_obj.save()
    print("Issue can be here in primary key victim", volunt_obj.pk)
    return HttpResponse(json.dumps({"victim_id": volunt_obj.id}), content_type="application/json")


def login(request):
    received_json_data = json.loads(request.body)
    number = received_json_data['mobile_number']
    password = received_json_data['password']
    volunt_data_list_active = list(Volunteers.objects.filter(
        number=number, password=password).values())
    if len(volunt_data_list_active) > 0:
        result_active = volunt_data_list_active[0]
        volunteer_details = {
            "id": result_active['id'],
            "name": result_active['name'],
            "location": result_active['location'],
            "status": result_active['status']
        }
        return HttpResponse(json.dumps({"volunteer_details": volunteer_details}), content_type="application/json")
    return HttpResponse(status=401)


def update_volunteer(request):
    received_json_data = json.loads(request.body)
    path = request.path
    volunteer_id = path.split('/')[1]
    vol_obj = Volunteers()
    vol_obj.transportation = received_json_data['has_vehicle']
    vol_obj.location = received_json_data['location']
    return HttpResponse(status=200)

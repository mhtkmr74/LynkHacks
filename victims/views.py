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
    victim_data_list_active = list(Victims.objects.filter(
        number=number, requirement_status=1).values())
    if len(victim_data_list_active) > 0:
        result_active = victim_data_list_active[0]
        victim_details = {
            "id": result_active['id'],
            "name": result_active['name'],
            "mobile": result_active['number'],
            "has_requirement": result_active['requirement_status']
        }
        return HttpResponse(json.dumps({"victim_details": victim_details}), content_type="application/json")
    victim_data_list = list(Victims.objects.filter(number=number).values())
    if len(victim_data_list) > 0:
        result = victim_data_list[0]
        victim_details = {
            "id": result['id'],
            "name": result['name'],
            "mobile": result['number'],
            "has_requirement": result['requirement_status']
        }
        return HttpResponse(json.dumps({"victim_details": victim_details}), content_type="application/json")
    else:
        return HttpResponse(status=400)


# def requirement_status(request):
#     path = request.path
#     requirement_id = path.split('/')[-1]
#     update_request_data = json.loads(request.body)
#     try:
#         vic_data_obj = Victims.objects.get(id=requirement_id)
#     except Exception as e:
#         print(e)
#         return HttpResponse(status=400)
#     vic_data_obj.Need = update_request_data['request_type']
#     vic_data_obj.Sub_need = update_request_data['value']
#     vic_data_obj.Comments = update_request_data['status']
#     vic_data_obj.save()

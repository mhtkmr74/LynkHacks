from django.shortcuts import render
import json
from .models import Victims, Requirements, Needs, SafeLocations
from django.http import HttpResponse
from math import sin, cos, sqrt, atan2, radians
from geopy.geocoders import Nominatim


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
    received_json_data = json.loads(request.body)
    number = received_json_data['mobile_number']
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


def requirement_status(request):
    path = request.path
    requirement_id = path.split('/')[-1]
    update_request_data = json.loads(request.body)
    try:
        vic_data_obj = Requirements.objects.get(id=requirement_id)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
    Type = update_request_data['request_type']
    sub_type = update_request_data['value']
    need_obj = Needs.objects.get(type=Type, sub_type=sub_type)
    vic_data_obj.delivery_status = update_request_data['status']
    vic_data_obj.requirement = need_obj
    vic_data_obj.save()


def get_safe_place(request):
    path = request.path
    vic_id = path.split('/')[1]
    vic_id_obj = Victims.objects.get(id=vic_id).values()
    present_location = vic_id_obj.location
    meters = 2000
    my_lat = present_location.split(',')[0]
    my_long = present_location.split(',')[1]
    coef = meters * 0.0000089
    new_lat_pos = my_lat + coef
    new_long_pos = my_long + coef / cos(my_lat * 0.018)
    new_lat_neg = my_lat - coef
    new_lon_neg = my_long - coef / cos(my_lat * 0.018)
    sf_complete_data = list(SafeLocations.objects.all().values())
    safe_places = list()
    for result in sf_complete_data:
        if result['lat'] > new_lat_neg and result['lon'] > new_lon_neg and result['lat'] < new_lat_pos and result['lon'] < new_lon_pos:
            safe_places.append({"lat": result['lat'], "long": result['lon']})
    return HttpResponse(json.dumps({"safe_places": safe_places}), content_type="application/json")


def safe_place(request):
    received_json_data = json.loads(request.body)
    location = received_json_data['safe_place']
    safe_place_object = SafeLocations()
    safe_place_object.location = location
    safe_place_object.save()
    return HttpResponse(status=200)


def all_requests(request):
    mappng = {
            "1": "Goods Foods",
            "2": "Goods Clothes",
            "3": "Goods Other_Accessories",
            "4": "Emergency ",
            "5": "Relocation "
        }
    path = request.path
    victim_id = path.split('/')[1]
    final_result = list()
    all_active_requirements = list(Requirements.objects.filter(
        victim_id=victim_id, delivery_status=5).values())
    for result in all_active_requirements:
        final_result.append({"request_id": result['id'], "need": mappng[result['requirement']].split()[
                            0], "sub_need":  ''.join(mappng[result['requirement']].split()[1:])})
    return HttpResponse(json.dumps(final_result), content_type="application/json")

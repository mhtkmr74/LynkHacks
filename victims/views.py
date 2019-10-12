from django.shortcuts import render
import json
from .models import Victims, Requirements, Needs, SafeLocations
from volunteers.models import Volunteers
from suppliers.models import Suppliers
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
    if not request.type == 'GET':
        victim_request(request)
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


def victim_request(request):
    path = request.path
    victim_id = path.split('/')[1]
    received_json_data = json.loads(request.body)
    request_type = received_json_data['request_type']
    value = received_json_data['value']
    quantity = received_json_data['quantity']
    need_obj = Needs.objects.get(type=request_type, sub_type=value)
    req_obj = Requirements()
    req_obj.requirement = need_obj
    req_obj.victim_id = Victims.objects.get(id=victim_id)
    req_obj.quantity = quantity
    req_obj.delivery_status = 1
    req_obj.save()
    metres = 500
    volunteer_id = -1
    present_victim_location = Victims.objects.get(id=victim_id).location
    present_victim_location_lat = present_victim_location['lat']
    present_victim_location_lon = present_victim_location['long']

    volunteers_complete_data = list(Volunteers.object.all().values())
    while volunteer_id < 0 and metres < 10000:
        coef = metres * 0.0000089

        new_lat_pos = present_victim_location_lat + coef
        new_long_pos = present_victim_location_lon + \
            coef / cos(present_victim_location_lon * 0.018)

        new_lat_neg = present_victim_location_lat - coef
        new_long_neg = present_victim_location_lon - \
            coef / cos(present_victim_location_lon * 0.018)

        for data in volunteers_complete_data:
            if data['location']['lat'] > new_lat_neg and data['location']['lat'] < new_lat_pos and data['location']['long'] > new_lat_neg and data['location']['long'] < new_long_pos:
                volunteer_id = data['id']
        metres += 500

    req_object = Requirements.objects.get(id=req_obj.id)
    if volunteer_id < 0:
        req_object.status = 7
        req_object.save()
        return
    req_object.status = 2
    req_object.save()
    supplier_complete_data = list(Needs.objects.filter(
        type=request_type, sub_type=value).values('suppliers__id', 'suppliers__location'))
    supplier_id = -1
    metres = 500
    present_vol_locatin = Volunteers.objects.get(id=volunteer_id).location'
    present_vol_locatin_lat = present_vol_locatin['lat']
    present_vol_locatin_lon = present_vol_locatin['long']
    while supplier_id < 0 and metres < 10000:
        coef = metres * 0.0000089

        new_lat_pos = present_vol_locatin_lat + coef
        new_long_pos = present_vol_locatin_lon + \
            coef / cos(present_vol_locatin_lon * 0.018)

        new_lat_neg = present_vol_locatin_lat - coef
        new_long_neg = present_vol_locatin_lon - \
            coef / cos(present_vol_locatin_lon * 0.018)

        for data in volunteers_complete_data:
            if data['location']['lat'] > new_lat_neg and data['location']['lat'] < new_lat_pos and data['location']['long'] > new_lat_neg and data['location']['long'] < new_long_pos:
                supplier_id = data['id']
        metres += 500

    req_object = Requirements.objects.get(id=req_obj.id)
    if supplier_id < 0:
        req_object.status = 7
        req_object.save()
        return  # to code
    req_object.status = 3
    req_object.save()
    victim_location = present_victim_location
    victim_mob = Victims.objects.get(id=victim_id).number
    supplier_location = Suppliers.objects.get(id=supplier_id).location
    supplier_mob = Suppliers.objects.get(id=supplier_id).number
    volunteer_location = present_vol_locatin
    volunteer_mob = Volunteers.objects.get(id=volunteer_id).number
    # function call
    return HttpResponse(json.dumps({"request_id": req_obj.id}))


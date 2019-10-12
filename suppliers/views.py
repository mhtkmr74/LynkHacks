from django.shortcuts import render
import json
from .models import Suppliers
from victims.models import Needs
from django.http import HttpResponse

# Create your views here.


def signup(request):
    received_json_data = json.loads(request.body)
    name = received_json_data['name']
    number = received_json_data['mobile_number']
    location = received_json_data['location']
    password = received_json_data['password']
    print("Issue possible in location")
    supp_obj = Suppliers()
    supp_obj.name = name
    supp_obj.number = number
    supp_obj.location = location
    supp_obj.save()
    print("Issue can be here in primary key victim", supp_obj.id)
    return HttpResponse(json.dumps({"victim_id": supp_obj.id}), content_type="application/json")


def login(request):
    received_json_data = json.loads(request.body)
    number = received_json_data['mobile_number']
    password = received_json_data['password']
    supplier_data_list_active = list(Suppliers.objects.filter(
        number=number, password=password).values())
    if len(supplier_data_list_active) > 0:
        result_active = supplier_data_list_active[0]
        supplier_details = {
            "id": result_active['id'],
            "name": result_active['name'],
            "location": result_active['location'],
            "status": result_active['status'],
            "quantity": result_active['quantity']
        }
        return HttpResponse(json.dumps({"supplier_details": supplier_details}), content_type="application/json")
    return HttpResponse(status=401)


def insert_goods(request):
    received_json_data = json.loads(request.body)
    path = request.path
    update_id = path.split('/')[1]
    goods = received_json_data['goods_type']
    res = Needs.objects.get(sub_type=goods)
    quantity = received_json_data['quantity']
    try:
        sup_upd = Suppliers.objects.get(id=update_id)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
    sup_upd.quantity = quantity
    sup_upd.donation = res
    sup_upd.save()
    return HttpResponse(status=200)






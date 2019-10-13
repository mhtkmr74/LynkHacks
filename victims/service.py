import requests


def sendMessages(victim_location, victim_mob, supplier_location, supplier_mob, volunteer_location, volunteer_mob):
    url = "https://www.fast2sms.com/dev/bulk"
    location = "Adyar"
    numbers = "9962256516, 8789813291"
    payload = "sender_id=FSTSMS&message={}&language=english&route=p&numbers={}".format(
        location, numbers)
    headers = {
        'authorization': "EGoanmHNs9qkv7jrTPRUZ8luVtfiYKI3OAeCJyxM6whBDXQ4WFGnrWH71ChiKUfS34vtOemFNajsMJbL",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

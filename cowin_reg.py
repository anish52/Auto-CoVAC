import requests
import datetime
import json
import telegram_send


def lambda_handler(event, context):
    # TODO implement
    state_code = 15 #Jharkhand
    district_id = 240 #Ranchi
    curr_date = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).date()
    
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}"\
            .format(district_id, curr_date.strftime("%d-%m-%Y"))
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)\
                                AppleWebKit/537.36 (KHTML, like Gecko)\
                                 Chrome/90.0.4430.93 Safari/537.36'}
    
    
    available_slots = {}
    response = requests.get(url, headers=headers)
    #response = requests.get(url)
    print(response)
    
    res_json = json.loads(response.text)
    
    for center in res_json['centers']:
        for session in center['sessions']:
            if session['min_age_limit'] == 45 and session['available_capacity'] > 0:
                m = '{} Slots of {} available @ {},{}-{} on {}.'\
                      .format(session['available_capacity'],session['vaccine'],\
                              center['name'],center['address'],center['pincode'],session['date'])
                print(m)
                telegram_send.send(messages = [m])
        break

    
    return {
        'statusCode': 200,
        'body': m
    }

lambda_handler(event = {}, context = None)
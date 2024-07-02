import json
import requests

def get_availability_by_date(date):
    result = requests.get("http://127.0.0.1:5001/availability/{}".format(date),
                          headers={'content-type':'application/json'})
    return result.json()

def add_new_booking(date,therapist_name,time,customer):
    booking={
        "date":date,
        "therapist_name":therapist_name,
        "time":time,
        "customer":customer
    }
    result = requests.put("http://127.0.0.1:5001/booking",headers={'content-type':'application/json'},
                          data = json.dumps(booking))

    print(f"Status Code: {result.status_code}")
    print(f"Response Text: {result.text}")


    return result.json()

def display_availability(records):
    for item in records:
        print("{:<20} {:<20} {:<20} ".format(item['name'],item['morning_hours'],item['evening_hours']))
        print("-"*100)

def run():
        print('**--------------------------------------------**')
        print(f'Hello there, welcome to wema therapy!')
        print('**--------------------------------------------**')
        print()
        date = input('What date you would like to book your appointment for (YYYY-MM-DD): ')
        print()
        slots = get_availability_by_date(date)
        print('--------------------------- AVAILABILITY --------------------------')
        print()
        display_availability(slots)
        print()
        place_booking = input('Would you like to book an appointment (y/n)?  ')

        book = place_booking == 'y'

        if book:
            therapist_name= input('Choose therapist (Ann or Amelia): ')
            time = input('Choose time based on availability (morning_hours or evening_hours?)')
            cust = input('Enter your name: ')
            add_new_booking(date, therapist_name, time, cust)
            print("Booking is Successful")
            print()
            slots = get_availability_by_date(date)
            display_availability(slots)

        print()
        print('See you soon!')


if __name__ == '__main__':
    run()
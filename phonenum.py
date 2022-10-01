from src.api import phoneapis
import requests


def number_scan():
    phonenum = input("Enter Mobile Number with country code : ")
    api_key = phoneapis()
    url = ("http://apilayer.net/api/validate?access_key="+api_key+"&number="+phonenum)
    resp = requests.get(url)
    details = resp.json()
    print('')
    print("Carrier : " + details['carrier'])
    print("Country Code : " + details['country_code'])
    print("Country : " + details['country_name'])
    print("Country Prefix: " + details['country_prefix'])
    print("Line Type : " + details['line_type'])
    print("International Format  : " + details['international_format'])
    print("Local Format : " + details['local_format'])
    print("Location : " + details['location'])
    print("Number : " + details['number'])
    print("Valid : " + details['valid'])



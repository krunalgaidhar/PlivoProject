import requests
from requests.auth import HTTPBasicAuth
from ptest.assertion import assert_equals
from pprint import pprint


# Get the List of Numbers
def get_list_of_numbers(url, auth_id, auth_token):
    list_of_numbers = requests.get(url + "/Number/", auth=HTTPBasicAuth(auth_id, auth_token))
    parsed_list_of_numbers = list_of_numbers.json()
    assert_equals(list_of_numbers.status_code, 200)
    print("Status Code : " + str(list_of_numbers.status_code))

    return parsed_list_of_numbers


# Get Any Two Numbers from List of Numbers
def get_any_two_numbers(list_of_numbers):
    number01 = list_of_numbers["objects"][0]["number"]
    number02 = list_of_numbers["objects"][1]["number"]
    two_numbers_map = {'number01': number01, 'number02': number02}

    return two_numbers_map


# Send Message from One Number to Another
def send_message(url, auth_id, auth_token, numbers_map):
    response_with_uuid = requests.post(url + "/Message/",
                                       auth=HTTPBasicAuth(auth_id, auth_token),
                                       data={"src": numbers_map['number01'], "dst": numbers_map['number02'],
                                             "text": "Sending Message"})
    parsed_response_with_uuid = response_with_uuid.json()
    assert_equals(response_with_uuid.status_code, 202)
    print("Status Code : " + str(response_with_uuid.status_code))
    message_uuid = parsed_response_with_uuid["message_uuid"][0]

    return message_uuid


# Get Actual Rate After Sending the Message
def get_actual_rate(url, auth_id, auth_token, message_uuid):
    response_my_message_rate = requests.get(url + "/Message/"+message_uuid+"/", auth=HTTPBasicAuth(auth_id, auth_token))
    parsed_response_my_message_rate = response_my_message_rate.json()
    assert_equals(response_my_message_rate.status_code, 200)
    print("Status Code : " + str(response_my_message_rate.status_code))

    return parsed_response_my_message_rate["total_rate"]


# Get Outbound Rate
def get_outbound_rate(url, auth_id, auth_token):
    price_response = requests.get(url + "/Pricing?country_iso=US", auth=HTTPBasicAuth(auth_id, auth_token))
    parsed_price_response = price_response.json()
    assert_equals(price_response.status_code, 200)
    print("Status Code : " + str(price_response.status_code))
    actual_message_rate = parsed_price_response["message"]["outbound_networks_list"][0]["rate"]

    return actual_message_rate


if __name__ == '__main__':
    authentication_id = 'MAODUZYTQ0Y2FMYJBLOW'
    authentication_token = 'ODgyYmQxYTQ2N2FkNDFiZTNhZWY4MDAwYWY4NzY0'
    basic_url = 'https://api.plivo.com/v1/Account/' + authentication_id

    print("\n -------------------- numbers list --------------------")
    numbers_list = get_list_of_numbers(basic_url, authentication_id, authentication_token)
    pprint(numbers_list)

    print("\n -------------------- two numbers list --------------------")
    two_numbers_dict = get_any_two_numbers(numbers_list)
    print(two_numbers_dict)

    print("\n -------------------- message uuid --------------------")
    uuid = send_message(basic_url, authentication_id, authentication_token, two_numbers_dict)
    print("message uuid : " + uuid)

    print("\n -------------------- my message rate --------------------")
    my_message_rate = get_actual_rate(basic_url, authentication_id, authentication_token, uuid)
    print("my message rate : " + my_message_rate)

    print("\n -------------------- outbound rate --------------------")
    outbound_rate = get_outbound_rate(basic_url, authentication_id, authentication_token)
    print("outbound rate : " + outbound_rate)
    assert_equals(my_message_rate, outbound_rate)




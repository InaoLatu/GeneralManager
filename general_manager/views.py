from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from GeneralManager import constants
import requests


def identification_telegram(request, **kwargs):
    request_string = constants.AUTH_SERVER_IP + "students/identification_telegram/" + kwargs['username'] + "/" + kwargs[
        'id']
    re = requests.get(request_string)
    return HttpResponse(re.text, status=re.status_code)


def check_user_exists(request, **kwargs):
    request_string = constants.AUTH_SERVER_IP + "students/check_user/" + kwargs['type'] + "/" + kwargs['id']
    re = requests.get(request_string)
    return HttpResponse(re.text, status=re.status_code)


def get_units(request, **kwargs):
    request_string = constants.AUTHORING_TOOL_IP + "units/"
    units_json = requests.get(request_string).json()
    return JsonResponse(units_json, safe=False)


def get_unit_microcontent(request, **kwargs):
    request_string = constants.STUDENT_MANAGER_IP + "student_manager/get_student_data/" + kwargs['id']
    student_data = requests.get(request_string).json()
    unit_found = False
    micro_content_list = {}
    for unit in student_data['progress']:
        if unit['name'] == kwargs['unit']:
            unit_found = True
            micro_content_list = unit['micro_contents'].copy()
            print(micro_content_list)
            break

    if unit_found:
        print("unit found")
        return JsonResponse(micro_content_list, safe=False)
    else:
        print("unit NOT found")
        print(kwargs['unit'])
        request_string = constants.AUTHORING_TOOL_IP + "units"
        #request_string = constants.GENERAL_MANAGER_IP + "get_units/"
        units_json = requests.get(request_string).json()
        for unit in units_json:
            if kwargs['unit'] == unit['name']:
                unit_id = unit['id']
        request_string = constants.STUDENT_MANAGER_IP + "student_manager/update_student_progress/" + kwargs['id'] + "/" + kwargs['unit'] + "/" + str(unit_id)
        micro_content_list = requests.get(request_string).json()
        return JsonResponse(micro_content_list, safe=False)


def get_microcontent(request, **kwargs):
    request_string = constants.AUTHORING_TOOL_IP + "microcontent?id=" + str(request.GET['id'])
    micro_content_json = requests.get(request_string).json()
    return JsonResponse(micro_content_json, safe=False)


@csrf_exempt
def store_mark(request, *args,**kwargs):
    global unit_id
    request_string = constants.AUTHORING_TOOL_IP + "units"
    units_json = requests.get(request_string).json()
    for unit in units_json:
        if request.POST['unit_name'] == unit['name']:
            unit_id = unit['id']

    data = {
        'student_id': request.POST['student_id'],
        'unit_id': unit_id,
        'microcontent_id': request.POST['microcontent_id'],
        'mark': request.POST['mark'],
    }

    print(data)
    request_string = constants.STUDENT_MANAGER_IP + "student_manager/store_mark"
    re = requests.post(request_string, data=data)
    return HttpResponse(re.text, status=re.status_code)

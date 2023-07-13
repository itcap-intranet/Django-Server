from ninja import NinjaAPI, Schema
from typing import List
from courses.models import Course
from courses.schemas import CourseSchema
from django.http import JsonResponse
import requests

api = NinjaAPI()
backend_host = 'http://localhost:5001' #backend

@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}

@api.get("/courses")
def get_courses(request):
    r = requests.get(backend_host + '/courses')
    return r.json()

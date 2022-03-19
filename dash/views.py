import json
import os
import pandas as pd

from rest_framework.decorators import api_view, authentication_classes, renderer_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from dash.rest.serializers import SkyUserSerializer, AttendanceCodeSerializer, PlannedAbsenceSerializer, StudentRequestSerializer, StudentSerializer, \
    StudentSerializer, AttendanceSerializer
from dash.rest.objects import Student, AttendanceCodes

from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError

from dash.rest.serializers import SkyUserSerializer, AttendanceSerializer
from dash.rest.permissions import AttendanceManager, Parent, Staff
from datetime import datetime
from .models import *
from .utils import *

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer])
def user(request):
    if request.method == "GET":
        user = SkyUserSerializer(request.user)           
        return Response(user.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([AttendanceManager])
def attendance(request):
    if request.method == 'POST':
        data = request.data
        if data.get('begin_date') and data.get('end_date'):
            data['begin_date'] = datetime.fromisoformat(data.get('begin_date').split('.')[0])
            data['end_date'] = datetime.fromisoformat(data.get('end_date').split('.')[0])
        serializer = AttendanceSerializer(data=request.data)
        print(serializer.is_valid())
        if not serializer.is_valid():
            return Response({"error":serializer.errors})
        serializer.save()
        return Response({"success": "Good job, boy"})


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([AttendanceManager])
@renderer_classes([JSONRenderer])
def student(request, student_id):
    if request.method == 'GET':
        result = calldb(f"SELECT id, first_name, last_name FROM tp_students WHERE student_id = {student_id}", request_type="single")
        if not result:
            return Response({
                "error":"Student Not Found"
            })  
        student = Student(id=result[0], first_name=result[1], last_name=result[2])   
        serialzer = StudentSerializer(student)
        return Response(serialzer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer])
def studentSearch(request):
    if request.method == "GET":
        print(request.auth)
        print(request.query_params.dict())
        student = Student(**request.query_params.dict())
        serializer = StudentRequestSerializer(student)
        stmt = f"""
        SELECT id, first_name, preferred_name, last_name, student_id
        FROM tp_students
        WHERE LOWER(first_name) LIKE '{stringToComparison(serializer.data['first_name'])}'
            AND LOWER(last_name) LIKE '{stringToComparison(serializer.data['last_name'])}'
            AND LOWER(grade_level) LIKE '{stringToComparison(serializer.data['grade_level'])}'
        LIMIT 20
        """
        print(stmt)
        result = calldb(stmt, request_type="mutliple")
        return Response({"Result":list(result)})
        
@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([AttendanceManager])
@renderer_classes([JSONRenderer])
def get_attendance_codes(request):
    # Calling the sky api
    results = calldb("select * from tp_attendance_codes", 'multiple')
    attendance = AttendanceCodes(codes=pd.DataFrame(results, columns=['id', 'name']).to_dict(orient='records'))
    serializer = AttendanceCodeSerializer(attendance)
    return JsonResponse(serializer.data)


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([Parent])
@renderer_classes([JSONRenderer])
def plan_absence(request):
    if request.method == "GET":
        return Response({"status":"sucess"})

    if request.method == "POST":
        # Loading planned absence data
        data = json.loads(request.body)

        # Form checking in case js doesn't work
        if data.get('child_id') == "":
            return Response({"error":"You need to select at least one child"})

        # Creating instance of an absence
        absence = PlannedAbsence(
            parent=request.user,
            child=data['child_id'],
            from_date=data['from_date'],
            to_date=data['to_date'],
            comment=data['comment']
        )
        absence.save()

        return Response({"status":"sucess"})
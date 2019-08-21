from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db import connection

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from traffic.models import *
from traffic.serializers import *

def checkout_view(request):
    return render(request, 'traffic/checkout.html')

def classroom_view(request):
    return render(request, 'traffic/classroom.html')

class ClassroomListCreate(generics.ListAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

@api_view(['POST'])
def checkout(request):
    family_number = request.data['family_number'].strip()
    checkout_type = request.data['checkout_type'].strip()
    if not family_number or (checkout_type != "walker" and checkout_type != "carline"):
        # print("missing data... Ignoring request")
        return Response({})
    try:
        f = Family.objects.get(family_number=family_number)
    except Family.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    c = Checkout.objects.create(family=f, is_walker=(checkout_type=='walker'))
    return Response({"family_id": c.family_id, "family_number": family_number, "checkout_type": checkout_type, "checkout_time": c.checkout_time})

@api_view(['POST'])
def cancel_checkout(request):
    fid = request.data['family_id']
    ct = request.data['checkout_time']
    if not fid or not ct:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        c = Checkout.objects.get(family_id=fid, checkout_time=ct)
    except Checkout.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    c.delete()
    return Response({"family_id": fid, "checkout_time": ct})

@api_view(['GET'])
def get_students(request, classroom_id):
    try:
        classroom = Classroom.objects.get(pk=classroom_id)
    except Classroom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    today = timezone.localdate()
    obj = []
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT S.first_name, S.last_name, C.is_walker
            FROM traffic_student S
            INNER JOIN (
                SELECT family_id, max(checkout_time) as checkout_time
                FROM traffic_checkout
                WHERE
                    DATE(checkout_time) = %s
                GROUP BY family_id
            ) T
            INNER JOIN traffic_checkout C
            WHERE
                S.family_id = C.family_id
                AND S.family_id = T.family_id
                AND C.checkout_time = T.checkout_time
                AND S.classroom_id = %s
        ''', [today, classroom_id])
        rows = cursor.fetchall()
        for r in rows:
            print(f"adding: {r}")
            if r:
                obj.append({
                    "first_name": r[0],
                    "last_name": r[1],
                    "is_walker": r[2],
                })
    return Response(obj)

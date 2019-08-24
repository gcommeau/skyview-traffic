import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db import connection
from django.contrib.auth.decorators import login_required

from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from traffic.models import *
from traffic.serializers import *

logger = logging.getLogger("traffic")

@login_required
def checkout_view(request):
    return render(request, 'traffic/checkout.html')

@login_required
def classroom_view(request):
    return render(request, 'traffic/classroom.html')

@login_required
def no_view(request):
    return redirect('/checkout')

class ClassroomListCreate(generics.ListAPIView):
    queryset = Classroom.objects.all().order_by("teacher")
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
def checkout(request):
    # Checking that the request is authenticated (user logged in)
    if not request.user.is_authenticated:
        logger.info("Received unauthenticated checkout request")
        return Response(status=status.HTTP_403_FORBIDDEN)
    logger.info(f"Received checkout request with data: {request.data}")
    # Getting request attributes and checking validity
    family_number = request.data['family_number'].strip()
    checkout_type = request.data['checkout_type'].strip()
    if not family_number or checkout_type not in [Checkout.TYPE_WALKER, Checkout.TYPE_CARLINE, Checkout.TYPE_PRESCHOOL]:
        logger.info("missing data... Ignoring request")
        return Response({})
    try:
        f = Family.objects.get(family_number=family_number)
    except Family.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # Creating new Checkout entry
    c = Checkout.objects.create(family=f, checkout_type=checkout_type)
    return Response({"family_id": c.family_id, "family_number": family_number, "checkout_type": checkout_type, "checkout_time": c.checkout_time})

@api_view(['POST'])
def cancel_checkout(request):
    # Checking that the request is authenticated (user logged in)
    if not request.user.is_authenticated:
        logger.info("Received unauthenticated cancel checkout request")
        return Response(status=status.HTTP_403_FORBIDDEN)
    logger.info(f"Received checkout cancel request with data: {request.data}")
    # Getting request attributes and checking validity
    fid = request.data['family_id']
    ct = request.data['checkout_time']
    if not fid or not ct:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # Deleting Checkout entry
    try:
        c = Checkout.objects.get(family_id=fid, checkout_time=ct)
    except Checkout.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    c.delete()
    return Response({"family_id": fid, "checkout_time": ct})

@api_view(['GET'])
def get_students(request, classroom_id):
    # Checking that the request is authenticated (user logged in)
    if not request.user.is_authenticated:
        logger.info("Received unauthenticated get students request")
        return Response(status=status.HTTP_403_FORBIDDEN)
    # Checking that the classroom ID is valid
    try:
        classroom = Classroom.objects.get(pk=classroom_id)
    except Classroom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # Querying database
    today = timezone.localdate()
    obj = []
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT S.first_name, S.last_name, C.checkout_type
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
            ORDER BY S.first_name, S.last_name
        ''', [today, classroom_id])
        rows = cursor.fetchall()
        for r in rows:
            print(f"adding: {r}")
            if r:
                obj.append({
                    "first_name": r[0],
                    "last_name": r[1],
                    "checkout_type": r[2],
                })
    return Response(obj)

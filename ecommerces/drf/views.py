# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework import authentication, permissions
from .serializers import (RegisterSerializer,LoginSerializer,UserRoleSerializer,UserRoleCreateSerializer,ProductSerializer,OrderSerializer)
from rest_framework import status
from rest_framework.authtoken.models import Token
from datetime import datetime
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ecommerces.pagination import CustomPagination
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.models import User
from drf.models import UserRole,Product,Order
import json
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf.decorator import is_valid_token

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)  
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

# Registration
class RegistrationAPI(APIView):
    """
    This API for Register User
    """
    def get(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid()
        user = serializer.save()
        if user:
            return Response({
                'username': user.username,
                'first_name':user.first_name,
                'status': status.HTTP_201_CREATED,
                'message':"User Register Sucessful ...!!"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Login
class LoginView(APIView):
    """
    This API for Login View
    """
    def get(self, request,format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid()
        user = serializer.validated_data.get("user")
        if user:
            token, created = Token.objects.get_or_create(user=user)
            user.last_login = datetime.now()
            user.save()
            return Response({"token": token.key}, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Logput
class LogoutView(APIView):
    """
    This API for Logout Views
    """
    permission_classes = (IsAuthenticated,TokenAuthentication)  
    def get(self, request):
        django_logout(request)
        return Response({
            'message': 'Logout Successful'
        })
    # or
    # token_key = request.META.get('HTTP_AUTHORIZATION', None)
    # token = token_key.replace('Token ', '')
    # Token.objects.get(key=token).delete()
    # return JsonResponse({
    #     'message': 'Logout Successful'
    # })

#create user role 
class UserRoleCreate(APIView):
    """
    This API for UserRoleCreate 
    """
    permission_classes = (IsAuthenticated,TokenAuthentication)  
    def get(self, request,format=None):
        serializer = UserRoleCreateSerializer(data=request.data)
        serializer.is_valid()
        user_role = serializer.save()
        if user_role:
            return Response({
                "id": user_role.id,
                "title": user_role.title,
                'is_active': user_role.is_active}, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#get list of userrole
class ListOfUserRole(APIView):
    """
    This API for ListOfUserRole 
    """
    permission_classes = (IsAuthenticated,)  
    def get(self, format=None):
        user_role_list = UserRole.objects.filter(is_active=1)
        serializer = UserRoleSerializer(user_role_list,many=True)
        return JsonResponse({'user_role_list': json.loads(json.dumps(serializer.data))})

#prodcut list function based
@csrf_exempt
@is_valid_token()
def product_list(request):
     """
    This API for display Product List
    """
    permission_classes = (IsAuthenticated,TokenAuthentication)
    queryset = Product.objects.all()
    serializer = ProductSerializer(data=queryset.data)
    return Response({'prodcut_list':serializer.data})

#create order
class OrderCreate(APIView):
    """
    This API for OrderCreate 
    """
    permission_classes = (IsAuthenticated,)  
    def get(self, request,format=None):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid()
        user_role = serializer.save()
        if user_role:
            return Response({
                "id": user_role.id,
                "title": user_role.title,
                'is_active': user_role.is_active}, status=200)

#list of order
class ListOfOrder(APIView):
    """
    This API for ListOfOrder 
    """
    permission_classes = (IsAuthenticated,TokenAuthentication,)  
    def get(self, format=None):
        user_role_list = User.objects.filter(is_active=1)
        serializer = OrderSerializer(user_role_list,many=True)
        return JsonResponse({'user_role_list': json.loads(json.dumps(serializer.data))})

#order place for use
class OrderPlace(APIView):
    permission_classes = (IsAuthenticated,TokenAuthentication,)  
    def get(self, request, format=None):
        token_key = request.META.get('HTTP_AUTHORIZATION', None)
        if token_key is not None:
            user_id = Token.objects.get(key=token_key).values_list('user_id', flat=True)
            if user_id:
                order_details = Order.objects.filter(user=user_id).first()
                order_item = OrderItem.objects.filter(orders=order_details.order_id)

            total = 0
            for rs in order_item:
                if rs.order_item.product == 'None':
                    total += rs.order_item.price * rs.quantity
                else:
                    total += rs.order_item.price * rs.quantity
            for rs in order_details:
                detail = OrderItem()
                detail.order_id     = data.id # Order Id
                detail.product_id   = rs.product_id
                detail.quantity     = rs.quantity
                detail.price = rs.variant.price
                detail.save()

            OrderItem.objects.filter(user=user_id).delete() # Clear & Delete OrderItem
            return Response({"messgae": "Your Order has been completed. Thank you "})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#accept order
class AcceptOrder(APIView):
    permission_classes = (IsAuthenticated,TokenAuthentication,)  
    def get(self, request, format=None):
        token_key = request.META.get('HTTP_AUTHORIZATION', None)
        if token_key is not None:
            user_id = Token.objects.get(key=token_key).values_list('user_id', flat=True)
            if user_id:
                order_details = Order.objects.filter(user=user_id).first()
                if order_details:
                    OrderItem.objects.create(
                        orders=order_id,
                        user=user_id,
                        customer_or_vendor=user_id,
                        order_status='Order Accepted'
                    )
                for item in order_details:
                    order_details.product.add(item)
                return Response({"message": 'Order Accepted'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#search prodcut 
@csrf_exempt
@is_valid_token()
def search_product(request):
    permission_classes = (IsAuthenticated,TokenAuthentication)  
    query = request.GET.get('query', None)
    if query is not None:
        qs1 = Product.objects.filter(product_name__icontains = query)
        qs3 = Product.objects.filter(price__icontains = query)
        result = qs1.union(qs2, qs3)
    else:
        result = Product.objects.none()
    context = {
        "result": result,
        "query": query
    }
    return Response(context)

#Custmization Pagination view for order list 
class PaginationView(GenericAPIView):
    """
    This API for Pagination View for Order List for easy to get no of data length 
    """
    serializer_class = OrderSerializer
    queryset = User.objects.all()  # query set data
    pagination_class = CustomPagination

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data  # pagination data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
        payload = {
            'return_code': '200',
            'return_message': 'Success',
            'data': data
        }
        return Response(data)
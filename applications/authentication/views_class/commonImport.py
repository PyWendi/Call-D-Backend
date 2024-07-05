from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
import json

# handle api controller
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# handle token Behavior
from rest_framework_simplejwt.authentication import JWTAuthentication

# Handle swagger action and decorator
from drf_yasg.utils import swagger_auto_schema

# Handle channel process
from applications.utilities.channel_method import trigger_channel

from rest_framework import viewsets, status
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from .models import Employee
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmployeeSerializer, TokenObtainPairSerializer
from rest_framework.views import exception_handler
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied as DRFPermissionDenied
from .error_messages import ERROR_MESSAGES

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TokenObtainPairSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()  
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status_code': status.HTTP_200_OK,
            'message': ERROR_MESSAGES['Success']['Retrieved']['message'],
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status_code': status.HTTP_200_OK,
            'message': ERROR_MESSAGES['Success']['Retrieved']['message'],
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'status_code': status.HTTP_201_CREATED,
            'message': ERROR_MESSAGES['Success']['Created']['message'],
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'status_code': status.HTTP_200_OK,
            'message': ERROR_MESSAGES['Success']['Updated']['message'],
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status_code': status.HTTP_200_OK,
            'message': ERROR_MESSAGES['Success']['Deleted']['message']
        }, status=status.HTTP_200_OK)
    
# Custom exception handler
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, ValidationError):
            error_info = ERROR_MESSAGES['ValidationError']
        elif isinstance(exc, NotFound) or isinstance(exc, Http404):
            error_info = ERROR_MESSAGES['NotFound']
        elif isinstance(exc, DRFPermissionDenied) or isinstance(exc, DjangoPermissionDenied):
            error_info = ERROR_MESSAGES['PermissionDenied']
        else:
            error_info = ERROR_MESSAGES['UnknownError']

        response.data = {
            'status_code': response.status_code,
            'error': error_info['message'],
            'error_code': error_info['code']
        }
    else:
        error_info = ERROR_MESSAGES['InternalServerError']
        response_data = {
            'status_code': 500,
            'error': error_info['message'],
            'error_code': error_info['code']
        }
        response = Response(response_data, status=500)

    return response

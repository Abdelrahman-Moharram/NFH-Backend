from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from django.db.models import Q
from rest_framework.permissions import AllowAny
from .models import User, Role
from .forms import user_form
from project.helper import to_int, paginate_query_set_list
from datetime import datetime, timezone
from .permissions import permission_allowed

from .serializers import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user_serial = UserSerial(data=[request.user], many=True)
    
    if not user_serial.is_valid():
        pass
    if len(user_serial.data)  < 1:
        return Response(
            data={'error':'no user data exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        data=user_serial.data[0],
        status=status.HTTP_200_OK
    )


class CustomTokenObtainPairView(TokenObtainPairView):
    serilizer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                secure=True,
                httponly=False,
                samesite='None',
                
                
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                secure=True,
                httponly=False,
                samesite='None',
                
            )

        return response


class CustomTokenRefreshView(TokenRefreshView):
    serilizer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                secure=True,
                httponly=False,
                samesite='None',
                
            )

        return response


class CustomTokenVerifyView(TokenVerifyView):
    serilizer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')

        if access_token:
            request.data['token'] = access_token

        return super().post(request, *args, **kwargs)




@permission_classes([AllowAny])
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response





############################ - USER MODULE - #################################

@api_view(['GET',])
@permission_allowed('permissions.users.view')
def get_list(request):
    if 'filter' in request.GET:
        users       = User.objects.order_by('created_at').filter(Q(full_name__contains=request.GET.get('filter', None))|Q(username__contains=request.GET.get('filter', None)))
        
    else:
        users       = User.objects.order_by('created_at').select_related('role').all()
    
    data            = paginate_query_set_list(users, request.GET)
    user_serial     = ListUserSerial(data['instances'], many=True)


    return Response(
        {
            'users'         : user_serial.data,
            "page"          : data['page'],
            "size"          : data['size'],
            "total_pages"   : data['total_pages'],
        }, 
        status=status.HTTP_200_OK
    )



@api_view(['GET',])
@permission_allowed('permissions.users.view')
def user_details(request, id):
    user = User.objects.select_related('role').filter(id=id).first()
    if not user:
        return Response(data={
                'message': "this user doesn't exist or has been deleted"
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    user_serial     = DetailedUserSerial(user)
    return Response(
        {
            'user': user_serial.data,
        }, 
        status=status.HTTP_200_OK
    )


@api_view(['GET',])
@permission_allowed('permissions.users.add')
def get_add_user_dropdowns(request):
    roles       = list(Role.objects.order_by('name').values('id', 'name'))


    return Response(
        {
            'roles':roles,
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST',])
@permission_allowed('permissions.users.add')
def add_user(request):
    form = user_form(data=request.POST)
    if form.is_valid():
        form.save()

        return Response({
                'message': f'user "{request.POST['full_name']}" added successfully'
            },
            status=status.HTTP_201_CREATED
        )
    return Response({
            'errors': form.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['PUT',])
@permission_allowed('permissions.users.edit')
def edit_user(request, id):
    user = User.objects.filter(id=id).first()
    if not user:
        return Response({
                'message': "this user doesn't exist or has been deleted"
            },
            status=status.HTTP_404_NOT_FOUND
        )
    form = user_form(data=request.POST, instance=user)
    if form.is_valid():
        form            = form.save(created_by=request.user)
        form.updated_by = request.user
        form.updated_at = datetime.now(tz=timezone.utc)

        form.save()

        return Response({
                'message': f'user "{request.POST['full_name']}" updated successfully'
            },
            status=status.HTTP_201_CREATED
        )
    return Response({
        'errors': form.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )



@api_view(['GET',])
@permission_allowed('permissions.users.view')
def user_search(request):
    if 'query' not in request.GET:
        return Response({'error':'you should enter a valid search value'})
    query   = request.GET['query']
    exclude = request.GET.get('exclude', None)

    users = User.objects.filter(
            Q(full_name__contains=query)|Q(username__contains=query)
        )
    if exclude:
        users = users.exclude(id=exclude)
    
    
    # users_serial = IncludedUserSerial(users.order_by('full_name'), many=True)

    users_list = list(users.order_by('full_name').values('id', 'username', 'full_name'))
    
    return Response(
        data={'users': users_list},
        status=status.HTTP_200_OK
    )

##############################################################################


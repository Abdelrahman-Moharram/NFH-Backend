from rest_framework.response import Response
from rest_framework import status

from accounts.permissions import permission_allowed
from project.helper import paginate_query_set_list
from rest_framework.decorators import api_view
from .models import Role, Role_Permission, Module
from .serializer import RolesListSerializer


@api_view(['GET',])
@permission_allowed('permissions.roles.view')
def list_roles(request):
    roles               = Role.objects.order_by('name').all() #.values('name', 'id', 'created_at', 'created_by')
    roles               = paginate_query_set_list(query_set=roles, params=request.GET)

    roles_serial        = RolesListSerializer(roles['instances'], many=True)


    return Response(
        {
            'roles'       : roles_serial.data,
            "page"          : roles['page'],
            "size"          : roles['size'],
            "total_pages"   : roles['total_pages'],
        }, 
        status=status.HTTP_200_OK
    )
    

@api_view(['GET',])
@permission_allowed('permissions.roles.view')
def role_details(request, id):
    role                = Role.objects.filter(id=id).first()
    if not role:
        return Response(
            {
                'error': "this role doesn't exist or may be deleted"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    list_permissions    = dict()
    modules             = Module.objects.filter(is_editable=True)
    role_permission     = Role_Permission.objects.filter(role=role)

    for module in modules:    
        list_permissions[module.name] = []
        for permission in  module.permissions.values('id', 'key', 'label'):
            perm_dict = dict(permission)
            if role_permission.filter(permission__id=permission['id']).exists():
                perm_dict['has_perm'] = True
            else:
                perm_dict['has_perm'] = False

            list_permissions[module.name].append(perm_dict)
        

    


    return Response(
        {
            'role'              : RolesListSerializer(role).data,
            'permissions'       : list_permissions,
        }, 
        status=status.HTTP_200_OK
    )
    
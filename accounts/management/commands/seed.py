from django.core.management.base import BaseCommand
from roles.models import Permission, Role, Role_Permission, Module

permissions_list = [
    {'module':'users', 'key':'permissions.users.view', 'label':'View Users'},
    {'module':'users', 'key':'permissions.users.add', 'label':'Add User'},
    {'module':'users', 'key':'permissions.users.edit', 'label':'Add User'},

    {'module':'roles', 'key':'permissions.roles.view', 'label':'View Roles'},
    {'module':'roles', 'key':'permissions.roles.add', 'label':'Add Role'},
    {'module':'roles', 'key':'permissions.roles.edit', 'label':'Edit Role'},
    {'module':'roles', 'key':'permissions.roles.edit.permissions', 'label':'Edit Role Permissions'},
]



class Command(BaseCommand):
    help = "seed database for testing and development."


    def handle(self, *args, **options):
        run_seed(self)


def run_seed(self):

    ########################################
    print('_'*100, "\n\n", "-"*20, 'seeding roles and each one permissions',"-"*20)
    role, _ = Role.objects.get_or_create(name='admin')
    role.save()

    for per in permissions_list:
        module, _       = Module.objects.get_or_create(name=per['module'])
        permission, _   = Permission.objects.get_or_create(key=per['key'], label=per['label'], module=module)
        

        Role_Permission.objects.get_or_create(role=role, permission=permission)
    #########################################
    print("\n", "-"*35, 'finished',"-"*35, '\n', '_'*100)



    
        
        
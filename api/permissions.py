from rest_framework.permissions import BasePermission


class Usercreation(BasePermission):
    def has_object_permission(self, request, view, obj):
        print("asdsa")
        if request.user and request.user.is_superuser:
            return True
        elif obj == request.user:
            return True
        return False
    def has_permission(self, request, view):
        print(request.method)
        if request.method!='GET':
            if  request.user and request.user.is_superuser:
                return True
            else:
                return False
        return True

class Articlecreation(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        else:
            print('geet hena leeh')
            return False
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method =='GET':
            return True
        elif request.user.is_authenticated and request.method =='POST':
            return True
        

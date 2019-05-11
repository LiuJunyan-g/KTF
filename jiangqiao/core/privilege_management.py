from rest_framework.views import APIView, Response
from core.forms import *
from core.models import *
from core.serializers import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from core.permission import *


class UserView(APIView):
    """get: 获取账户列表"""
    """post: 新建账户"""
    """put: 修改账户"""
    """delete: 删除账户"""

    def get_object(self, pk):
        try:
            return User.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'user', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        user = User.objects.all().exclude(id=1).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + limit]
        count = User.objects.count()
        seriz = UserListSerializer(user, many=True)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功', 'count': count})

    #
    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'user', 'add'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        username = request.data.get('username')
        if User.objects.filter(username=username).first():
            return Response({'result': '0', 'message': '创建失败，该用户已存在'})
        department = None
        department_id = request.data.get('department_id')
        if department_id:
            department = Department.objects.filter(id=department_id).first()
        form = UserForm(request.data)
        if form.is_valid():
            data = form.cleaned_data
            try:
                new_user = User.objects.create(username=data['username'], name=data['name'],
                                               role_id=data['role_id'], department_id=department)
                new_user.set_password(data['password'])
                new_user.save()
            except:
                return Response({'result': '0', 'message': '创建失败'})
            return Response({'result': '1', 'message': '创建成功'})
        return Response({'result': '0', 'message': '数据不完整' + str(form.errors)})

    def put(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'user', 'change'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        view_user = self.get_object(pk)
        username = request.data.get('username')
        if username and not view_user.username == username:
            view_user.username = username
        name = request.data.get('name')
        if name and not view_user.name == name:
            view_user.name = name
        password = request.data.get('password')
        if password and not view_user.password == password:
            view_user.set_password(password)
        role_id = request.data.get('role_id')
        if role_id:
            role = Group.objects.filter(id=int(role_id)).first()
            if role and not role == view_user.role_id:
                view_user.role_id = role
        department_id = request.data.get('department_id')
        if department_id:
            department = Department.objects.filter(id=int(department_id)).first()
            view_user.department_id = department
        view_user.save()
        return Response({'result': '1', 'message': '修改成功'})


    def delete(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'user', 'delete'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        view_user = self.get_object(pk)
        view_user.delete()
        return Response({'result': '1'})


class UserDetailView(APIView):
    """获取用户详情"""

    def get_object(self, pk):
        try:
            return User.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'user', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        view_user = self.get_object(pk)  # 查看的user
        seriz = UserDetailSerializer(view_user)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功'})


class RoleView(APIView):
    """get: 获取角色列表"""

    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在!'})
        roles = Group.objects.all()
        seriz = RoleSerializer(roles, many=True)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功'})


class DepartmentView(APIView):
    """get: 获取部门列表"""
    """post: 新建部门"""
    """put: 修改部门"""
    """delete: 删除部门"""

    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'department', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        type = request.GET.get('type', 1)
        departments = Department.objects.filter(type=type).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + limit]
        count = Department.objects.filter(type=type).count()
        seriz = DepartmentListSerializer(departments, many=True)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功', 'count': count})

    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'department', 'add'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        village_id = request.data.get('village_id')
        village = Village.objects.filter(id=village_id).first()
        type = request.data.get('type')
        name = request.data.get('name')
        if not name:
            return Response({'result': '0', 'message': '无部门名称!'})
        if Department.objects.filter(name=name, type=type).first():
            return Response({'result': '0', 'message': '该部门已存在'})
        try:
            Department.objects.create(name=name, type=type, village_id=village)
        except:
            return Response({'result': '0', 'message': '创建失败'})
        return Response({'result': '1', 'message': '创建成功'})

    def put(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'department', 'change'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        name = request.data.get('name')
        if not name:
            return Response({'result': '0', 'message': '无部门名称!'})
        department = Department.objects.filter(id=pk).first()
        try:
            department.name = name
            department.save()
        except:
            return Response({'result': '0', 'message': '修改失败'})
        return Response({'result': '1', 'message': '修改成功'})

    def get_object(self, pk):
        try:
            return Department.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def delete(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'department', 'delete'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        department = self.get_object(pk)
        department.delete()
        return Response({'result': '1', 'message': '删除成功'})


# 修改密码
class ChangePassword(APIView):
    def put(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        current_password = request.data.get('current_password')
        if not user.check_password(current_password):
            return Response({'result': '0', 'message': '原密码不正确'})
        new_password = request.data.get('new_password')
        user.set_password(new_password)
        user.save()
        return Response({'result': '1', 'message': '修改密码成功'})

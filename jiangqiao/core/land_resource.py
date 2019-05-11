from core.serializers import *
from rest_framework.views import APIView, Response
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from core.forms import *
from core.models import *
from core.permission import *


class LandResourceListView(APIView):
    """get:获取土地资源列表"""
    """post:新建土地资源"""

    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'landresource', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        min_floor_space = request.GET.get('min_floor_space')
        max_floor_space = request.GET.get('max_floor_space')
        min_plot_ratio = request.GET.get('min_plot_ratio')
        max_plot_ratio = request.GET.get('max_plot_ratio')
        condition = {
        }
        if user.is_village_department():
            condition['user_id__department_id'] = user.department_id
        elif user.is_town_department():
            project_ids = user.get_progresses().values_list('project_id', flat=True)
            condition['project_ids__in'] = project_ids
        if min_floor_space and max_floor_space:
            condition['floor_space__gte'] = min_floor_space
            condition['floor_space__lte'] = max_floor_space
        if min_plot_ratio and max_plot_ratio:
            condition['plot_ratio__gte'] = min_plot_ratio
            condition['plot_ratio__lte'] = max_plot_ratio

        state = request.GET.get('state')
        if state:
            condition['state'] = state
        land_resource = LandResource.objects.filter(**condition).order_by('-id')[
                        (page - 1) * 10:(page - 1) * 10 + limit]
        count = LandResource.objects.filter(**condition).count()
        seriz = LandResourceListSerializer(land_resource, many=True)
        print(seriz.data)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功', 'count': count})

    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'landresource', 'add'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        form = LandResourceForm(request.data)
        # print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                land = LandResource.objects.create(state=data['state'], location=data['location'],
                                                   vacant_area=data['vacant_area'],
                                                   ground_situation=data['ground_situation'],
                                                   land_nature=data['land_nature'],
                                                   domicile=data['domicile'],
                                                   floor_space=data['floor_space'],
                                                   plot_ratio=data['plot_ratio'],
                                                   max_height=data['max_height'],
                                                   lease_month=data['lease_month'],
                                                   residue_month=data['residue_month'],
                                                   remark=data['remark'], user_id=user,
                                                   department_id=user.department_id)
            except:
                return Response({'result': '0', 'message': '创建失败'})
            return Response({'result': '1', 'message': '创建成功', 'data': {'land_record_id': land.id}})
        return Response({'result': '0', 'message': '数据不完整'})


class LandResourceDetailView(APIView):
    """get：获取土地资源详情"""
    """put: 更改土地资源详情"""

    def get_object(self, pk):
        try:
            return LandResource.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'landresource', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        land_resource = self.get_object(pk)
        print(land_resource)
        seriz = LandResourceDetailSerializer(land_resource)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功'})

    def put(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'landresource', 'change'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        land = LandResource.objects.filter(id=pk).first()
        form = LandResourceForm(request.data)
        if form.is_valid():
            data = form.cleaned_data
            land.state = data['state']
            land.location = data['location']
            land.vacant_area = data['vacant_area']
            land.ground_situation = data['ground_situation']
            land.land_nature = data['land_nature']
            land.domicile = data['domicile']
            land.floor_space = data['floor_space']
            land.plot_ratio = data['plot_ratio']
            land.max_height = data['max_height']
            land.lease_month = data['lease_month']
            land.residue_month = data['residue_month']
            land.remark = data['remark']
            land.save()
            return Response({'result': '1', 'message': '修改成功'})
        return Response({'result': '0', 'message': '数据不完整'})


class LandResourceDeleteView(APIView):
    """post:删除勾选的土地资源"""

    def get_object(self, pk):
        try:
            return LandResource.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def delete(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'landresource', 'delete'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        land = self.get_object(pk)
        land.delete()
        return Response({'result': '1', 'message': '删除成功'})

from core.serializers import *
from rest_framework.views import APIView, Response
from core.forms import *
from core.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from core.permission import *


class BuildingResourceListView(APIView):
    """get:获取楼宇资源列表"""
    """post:新建楼宇资源"""

    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'buildingresource', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        min_floor_space = request.GET.get('min_floor_space')
        max_floor_space = request.GET.get('max_floor_space')
        min_covered_area = request.GET.get('min_covered_area')
        max_covered_area = request.GET.get('max_covered_area')
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
        if min_covered_area and max_covered_area:
            condition['covered_area__gte'] = min_covered_area
            condition['covered_area__lte'] = max_covered_area
        state = request.GET.get('state')
        if state:
            condition['state'] = state
        building_resources = BuildingResource.objects.filter(**condition).order_by('-id')[(page-1)*10:(page-1)*10 + limit]
        count = BuildingResource.objects.filter(**condition).count()  # TODO:跟上面过滤条件一直
        seriz = BuildingResourceListSerializer(building_resources, many=True)
        print(seriz.data)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功', 'count': count})

    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'buildingresource', 'add'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        request_data = request.data
        print(request_data)
        form = BuildingResourceForm(request_data)
        if form.is_valid():
            data = form.cleaned_data
            # try:
            building = BuildingResource.objects.create(user_id=user, name=data['name'],
                                                       location=data['location'],
                                                       property=data['property'], state=data['state'],
                                                       sewage_pipe=data['sewage_pipe'], plies=data['plies'],
                                                       floor_space=data['floor_space'],
                                                       covered_area=data['covered_area'],
                                                       vacant_area=data['vacant_area'],
                                                       produce_evidence=data['produce_evidence'],
                                                       lease_month=data['lease_month'],
                                                       residue_month=data['residue_month'], remark=data['remark'],
                                                       department_id=user.department_id)
            # print('111', request.data.get('building'))
            # except:
            # return Response({'result': '0', 'message': '创建失败'})
            return Response({'result': '1', 'message': '创建成功', 'data': {'building_record_id': building.id}})
        return Response({'result': '0', 'message': '数据不完整', 'm': str(form.errors)})


class BuildingResourceDetailView(APIView):
    """get：获取楼宇资源详情"""
    """post: 更改楼宇资源详情"""

    def get_object(self, pk):
        try:
            return BuildingResource.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'buildingresource', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        building_resource = self.get_object(pk)
        seriz = BuildingResourceDetailSerializer(building_resource)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功'})

    def put(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'buildingresource', 'change'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        building = BuildingResource.objects.filter(id=pk).first()
        form = BuildingResourceForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            building.name = data['name']
            building.location = data['location']
            building.property = data['property']
            building.state = data['state']
            building.sewage_pipe = data['sewage_pipe']
            building.plies = data['plies']
            building.floor_space = data['floor_space']
            building.covered_area = data['covered_area']
            building.vacant_area = data['vacant_area']
            building.produce_evidence = data['produce_evidence']
            building.lease_month = data['lease_month']
            building.residue_month = data['residue_month']
            building.remark = data['remark']
            building.save()
            return Response({'result': '1', 'message': '修改成功'})
        return Response({'result': '0', 'message': '数据不完整'})


class BuildingResourceDeleteView(APIView):
    """post:删除勾选的楼宇资源"""

    def get_object(self, pk):
        try:
            return BuildingResource.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def delete(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'buildingresource', 'delete'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        building = self.get_object(pk)
        building.delete()
        return Response({'result': '1', 'message': '获取成功'})

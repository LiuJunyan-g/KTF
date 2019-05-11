from core.serializers import *
from rest_framework.views import APIView, Response
from core.forms import *
from core.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from core.permission import *


class PlantResourceListView(APIView):
    """get:获取厂房资源列表"""
    """post:新建厂房资源"""

    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'plantresource', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        min_floor_space = request.GET.get('min_floor_space')
        max_floor_space = request.GET.get('max_floor_space')
        min_covered_area = request.GET.get('min_covered_area')
        max_covered_area = request.GET.get('max_covered_area')
        # print(min_floor_space)
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
        plant_resource = PlantResource.objects.filter(**condition).order_by('-id')[(page-1)*10:(page-1)*10 + limit]
        count = PlantResource.objects.filter(**condition).count()  # TODO:跟上面过滤条件一直
        seriz = PlantResourceListSerializer(plant_resource, many=True)
        print(seriz.data)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功', 'count': count})

    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'plantresource', 'add'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        form = PlantResourceForm(request.data)
        print('111', form.errors)

        if form.is_valid():
            data = form.cleaned_data
            print(data['produce_evidence'])
            # try:
            plant = PlantResource.objects.create(user_id=user, name=data['name'],
                                                 location=data['location'],
                                                 property=data['property'], state=data['state'],
                                                 sewage_pipe=data['sewage_pipe'], plies=data['plies'],
                                                 floor_space=data['floor_space'],
                                                 covered_area=data['covered_area'],
                                                 produce_evidence=data['produce_evidence'],
                                                 vacant_area=data['vacant_area'],
                                                 lease_month=data['lease_month'],
                                                 residue_month=data['residue_month'], remark=data['remark'],
                                                 department_id=user.department_id)
            # except:
            # return Response({'result': '0', 'message': '创建失败'})
            return Response({'result': '1', 'message': '创建成功', 'data': {'plant_record_id': plant.id}})
        return Response({'result': '0', 'message': '数据不完整'})


class PlantResourceDetailView(APIView):
    """get：获取厂房资源详情"""
    """put: 更改厂房资源详情"""

    def get_object(self, pk):
        try:
            return PlantResource.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'plantresource', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        plant_resource = self.get_object(pk)
        seriz = PlantResourceDetailSerializer(plant_resource)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功'})

    def put(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'plantresource', 'change'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        plant = PlantResource.objects.filter(id=pk).first()
        form = PlantResourceForm(request.data)
        if form.is_valid():
            data = form.cleaned_data
            plant.name = data['name']
            plant.location = data['location']
            plant.property = data['property']
            plant.state = data['state']
            plant.sewage_pipe = data['sewage_pipe']
            plant.plies = data['plies']
            plant.floor_space = data['floor_space']
            plant.produce_evidence = data['produce_evidence']
            plant.covered_area = data['covered_area']
            plant.vacant_area = data['vacant_area']
            plant.lease_month = data['lease_month']
            plant.residue_month = data['residue_month']
            plant.remark = data['remark']
            plant.save()
            return Response({'result': '1', 'message': '修改成功'})
        return Response({'result': '0', 'message': '数据不完整'})


class PlantResourceDeleteView(APIView):
    """post:删除勾选的厂房资源"""

    def get_object(self, pk):
        try:
            return PlantResource.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def delete(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'plantresource', 'delete'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        plant = self.get_object(pk)
        plant.delete()
        return Response({'result': '1', 'message': '获取成功'})

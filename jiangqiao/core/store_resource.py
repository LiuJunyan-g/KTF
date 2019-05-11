from core.serializers import *
from rest_framework.views import APIView, Response
from core.forms import *
from core.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from core.permission import *

class StoreResourceListView(APIView):
    """get:获取商铺资源列表"""
    """post:新建商铺资源"""

    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'storeresource', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        min_total_area = request.GET.get('min_total_area')
        max_total_area = request.GET.get('max_total_area')
        # print(min_floor_space)
        condition = {
        }
        if user.is_village_department():
            condition['user_id__department_id'] = user.department_id
        elif user.is_town_department():
            project_ids = user.get_progresses().values_list('project_id', flat=True)
            condition['project_ids__in'] = project_ids
        if min_total_area and max_total_area:
            condition['total_area__gte'] = min_total_area
            condition['total_area__lte'] = max_total_area
        state = request.GET.get('state')
        if state:
            condition['state'] = state
        store_resource = StoreResource.objects.filter(**condition).order_by('-id')[(page-1)*10:(page-1)*10 + limit]

        count = StoreResource.objects.filter(**condition).count()  # TODO:跟上面过滤条件一直
        seriz = StoreResourceListSerializer(store_resource, many=True)
        print(seriz.data)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功', 'count': count})

    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'storeresource', 'add'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        form = StoreResourceForm(request.data)
        if form.is_valid():
            data = form.cleaned_data
            # try:
            store = StoreResource.objects.create(user_id=user, name=data['name'],
                                                 location=data['location'],
                                                 state=data['state'],
                                                 plies=data['plies'],
                                                 produce_evidence=data['produce_evidence'],
                                                 sewage_pipe=data['sewage_pipe'], total_area=data['total_area'],
                                                 lease_month=data['lease_month'], vacant_area=data['vacant_area'],
                                                 residue_month=data['residue_month'], remark=data['remark'],
                                                 department_id=user.department_id)
            # except:
            # return Response({'result': '0', 'message': '创建失败'})
            return Response({'result': '1', 'message': '创建成功'})
        return Response({'result': '0', 'message': '数据不完整'})


class StoreResourceDetailView(APIView):
    """get：获取商铺资源详情"""
    """put: 更改商铺资源详情"""

    def get_object(self, pk):
        try:
            return StoreResource.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'storeresource', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        store_resource = self.get_object(pk)
        seriz = StoreResourceDetailSerializer(store_resource)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功'})

    def put(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'storeresource', 'change'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        store = StoreResource.objects.filter(id=pk).first()
        form = StoreResourceForm(request.data)
        if form.is_valid():
            data = form.cleaned_data
            store.state = data['state']
            store.name = data['name']
            store.location = data['location']
            store.plies = data['plies']
            store.produce_evidence = data['produce_evidence']
            store.sewage_pipe = data['sewage_pipe']
            store.total_area = data['total_area']
            store.lease_month = data['lease_month']
            store.vacant_area = data['vacant_area']
            store.residue_month = data['residue_month']
            store.remark = data['remark']
            store.save()
            return Response({'result': '1', 'message': '修改成功', 'data': {}})
        return Response({'result': '0', 'message': '数据不完整'})


class StoreResourceDeleteView(APIView):
    """post:删除勾选的商铺资源"""

    def get_object(self, pk):
        try:
            return StoreResource.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def delete(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'storeresource', 'delete'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        store = self.get_object(pk)
        store.delete()
        return Response({'result': '1'})

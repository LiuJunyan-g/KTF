from core.serializers import *
from rest_framework.views import APIView, Response
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import datetime
from core.permission import *


class NoticeListView(APIView):
    """get:获取通知列表"""
    """post:新建通知"""

    def get(self, request):
        user_id = request.GET.get('user_id', 1)
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'notice', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        notices = Notice.objects.all().order_by('-id')[(page - 1) * 10:(page - 1) * 10 + limit]
        count = Notice.objects.count()
        seriz = NoticeListSerializer(notices, many=True, context={'user': user})
        print(seriz.data)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功', 'count': count})

    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'notice', 'add'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        notice_type = request.data.get('type')
        name = request.data.get('name')
        if notice_type == '1':
            file = request.data.get('file')
            if not file:
                return Response({'result': '0', 'message': '缺少文件'})
            try:
                Notice.objects.create(user_id=user, name=file.name.split('.')[0], type=notice_type, file=file)
            except:
                return Response({'result': '0', 'message': '创建失败'})
            return Response({'result': '1', 'message': '创建成功'})
        elif notice_type == '2':
            content = request.data.get('content')
            try:
                Notice.objects.create(user_id=user, name=name, type=notice_type, content=content)
            except:
                return Response({'result': '0', 'message': '创建失败'})
            return Response({'result': '1', 'message': '创建成功'})
        else:
            return Response({'result': '1', 'message': '缺少notice_type'})


class NoticeDetailView(APIView):
    """get：获取通知详情"""

    def get_object(self, pk):
        try:
            return Notice.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'notice', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        notice = self.get_object(pk)
        seriz = NoticeDetailSerializer(notice)
        if not user.read_records.filter(notice_id=notice).first():
            NoticeReadRecord.objects.create(user_id=user, notice_id=notice)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功'})


class NoticeDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Notice.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def delete(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'notice', 'delete'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        notice = self.get_object(pk)
        notice.delete()
        return Response({'result': '1', 'message': '删除成功'})
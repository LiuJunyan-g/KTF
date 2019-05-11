from rest_framework.views import APIView, Response
from core.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from core.permission import *


class ProjectFileView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'projectfile', 'add'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        project_id = request.data.get('project_id')
        project = Project.objects.filter(id=int(project_id)).first()
        if not project:
            return Response({'result': '0', 'message': '该项目不存在'})
        file_type = request.data.get('file_type')
        if not file_type:
            return Response({'result': '0', 'message': '缺少file_type'})
        file = request.data.get('file')
        if not file:
            return Response({'result': '0', 'message': '缺少file'})
        try:
            file_upload = ProjectFile.objects.create(file_name=file.name.split('.')[0], file_type=file_type, file=file,
                                                     project_id=project)
        except Exception as e:
            return Response({'result': '0', 'message': '上传文件失败'+str(e)})
        return Response({'data': file_upload.id, 'result': '1', 'message': '上传成功'})


class ProjectFileDeleteView(APIView):
    def get_object(self, pk):
        try:
            return ProjectFile.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def delete(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'projectfile', 'delete'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        file = self.get_object(pk)
        file.delete()
        return Response({'result': '1', 'data': {}, 'message': '删除成功'})
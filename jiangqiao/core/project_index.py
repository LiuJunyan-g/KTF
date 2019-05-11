from rest_framework.views import APIView, Response
from core.models import *
from django.db.models import Q


class ProjectIndexView(APIView):
    def get(self, request):

        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if user.is_mayor() or user.is_center() or user.is_town_department():
            trial_project = Project.objects.filter(state__in=['1', '2', '3']).count()
            approved_project = Project.objects.filter(state='4').count()
            reject_project = Project.objects.filter(state='5').count()
            type1_project_count = Project.objects.filter(type='1').count()
            type2_project_count = Project.objects.filter(type='2').count()
            type3_project_count = Project.objects.filter(type='3').count()
            type4_project_count = Project.objects.filter(type='4').count()
            return Response({'data': {"trial_project": trial_project,
                                      "approved_project": approved_project,
                                      "reject_project": reject_project,
                                      "type1_project_count": type1_project_count,
                                      "type2_project_count": type2_project_count,
                                      "type3_project_count": type3_project_count,
                                      "type4_project_count": type4_project_count
            }, 'result': '1', 'message': '获取成功'})
        elif user.is_village_department():
            projects = Project.objects.filter(
                user_id__department_id=user.department_id)  # 当前用户所在部门下的所有项目
            trial_project = projects.filter(state__in=['1', '2', '3']).count()
            approved_project = projects.filter(state='4').count()
            reject_project = projects.filter(state='5').count()
            type1_project_count = projects.filter(type='1').count()
            type2_project_count = projects.filter(type='2').count()
            type3_project_count = projects.filter(type='3').count()
            type4_project_count = projects.filter(type='4').count()
            return Response({'data': {"trial_project": trial_project,
                                      "approved_project": approved_project,
                                      "reject_project": reject_project,
                                      "type1_project_count": type1_project_count,
                                      "type2_project_count": type2_project_count,
                                      "type3_project_count": type3_project_count,
                                      "type4_project_count": type4_project_count
            }, 'result': '1', 'message': '获取成功'})
        else:
            return Response({'data': {}, 'result': '0', 'message': '获取失败'})


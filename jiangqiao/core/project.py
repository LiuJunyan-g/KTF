from core.serializers import *
from rest_framework.views import APIView, Response
from core.forms import *
from core.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import datetime
from core.views import generate_project_number
from core.permission import *


class ProjectView(APIView):
    """新建前，生成项目的序号"""

    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'project', 'add'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        type = request.GET.get('type')
        number = generate_project_number(type)
        return Response({'result': '1', 'message': '成功', 'data': number})


class ProjectListView(APIView):
    """get:获取总库列表页"""

    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'project', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        start = int(request.GET.get('page', 1))
        size = int(request.GET.get('limit', 10))
        min_used_areas = request.GET.get('min_used_areas')
        max_used_areas = request.GET.get('max_used_areas')
        menu_type = request.GET.get('menu_type')
        menu_state = request.GET.get('menu_state')
        color = request.GET.get('color')
        condition = {
            'type__in': ['1', '2', '3', '4'],
            'state__in': ['0', '1', '2', '3', '4', '5'],
        }
        if user.is_village_department():
            condition['user_id__department_id'] = user.department_id
        if min_used_areas and max_used_areas:
            condition['used_areas__gte'] = min_used_areas
            condition['used_areas__lte'] = max_used_areas

        if menu_type == '1':  # 租赁
            condition['type__in'] = ['1', '2']
        elif menu_type == '2':  # 拟出让
            condition['type__in'] = ['3']
        elif menu_type == '3':  # 历史存量
            condition['type__in'] = ['4']

        if menu_state == '1':  # 否决
            condition['state__in'] = ['5']
        elif menu_state == '2':  # 获批
            condition['state__in'] = ['4']
        elif menu_state == '3':  # 在审
            condition['state__in'] = ['1', '2', '3']

        if user.is_town_department():  # 若为镇级部门
            if user.get_trial_progresses():
                condition['id__in'] = user.get_trial_progresses().values_list('project_id', flat=True)
            else:
                condition['id__in'] = []
        elif user.is_village_department():  # 若为村级部门
            condition['user_id__department_id'] = user.department_id

        if color:  # 铃铛需要传值
            progresses = None
            if color == 'yellow':
                progresses = user.get_yellow_progresses()
            elif color == 'green':
                progresses = user.get_green_progresses()
            elif color == 'red':
                progresses = user.get_red_progresses()
            if progresses:
                project_ids = progresses.values_list('project_id', flat=True)
            else:
                project_ids = []
            condition = {'id__in': project_ids}
        print('条件',condition)
        projects = Project.objects.filter(**condition).order_by('-id')[(start - 1) * 10:(start - 1) * 10 + size]
        count = Project.objects.filter(**condition).count()
        seriz = ProjectListSerializer(projects, many=True)
        print(seriz.data)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功', 'count': count})


class SupplyLandProjectView(APIView):
    """get:查看供地类项目详情"""
    """post:新建供地类项目"""
    """put:修改供地类项目"""

    def get_object(self, pk):
        try:
            return Project.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'project', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        supply_land = self.get_object(pk)
        seriz = SupplyLandDetailSerializer(supply_land)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功'})

    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'project', 'add'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        form = SupplyLandForm(request.data)
        if form.is_valid():
            data = form.cleaned_data
            state = data['state']
            print(state)
            try:
                project = Project.objects.create(user_id=user,
                                                 state=data['state'], apply_date=data['apply_date'],
                                                 name=data['name'], type=data['type'],
                                                 used_areas=data['used_areas'], covered_area=data['covered_area'],
                                                 plot_ratio=data['plot_ratio'],
                                                 project_four_to_scope=data['project_four_to_scope'],
                                                 project_address=data['project_address'],
                                                 use_land_type=data['use_land_type'], investor=data['investor'],
                                                 project_introduction=data['project_introduction'],
                                                 holding_main=data['holding_main'],
                                                 investment_properties=data['investment_properties'],
                                                 registered_fund=data['registered_fund'],
                                                 aggregate_investment=data['aggregate_investment'],
                                                 estimated_sales=data['estimated_sales'],
                                                 estimated_tax=data['estimated_tax'],
                                                 contact_people=data['contact_people'],
                                                 contact_way=data['contact_way'],
                                                 docking_domain=data['docking_domain'])
            except Exception as e:
                return Response(
                    {'result': '0', 'message': '创建失败,' + str(e) + 'state:' + data['state'] + 'type:' + data['type']})
            project.number = generate_project_number(data['type'], project.id)
            if data['land_resource_ids']:
                project.land_resources.set(data['land_resource_ids'])
            if data['plant_resource_ids']:
                project.plant_resources.set(data['plant_resource_ids'])
            if data['building_resource_ids']:
                project.building_resources.set(data['building_resource_ids'])
            if data['store_resource_ids']:
                project.store_resources.set(data['store_resource_ids'])
            project.save()
            if not project.progresses.filter(user_id__isnull=False).first():
                ProjectProgress.objects.create(project_id=project, result='3', start_time=datetime.datetime.now(),
                                               user_id=user)
            if state == '1':  # 提交
                group = Group.objects.filter(name='产促中心').first()  # TODO:隐患
                ProjectProgress.objects.create(project_id=project, start_time=datetime.datetime.now(), role_id=group)

            # files_data = request.data.get('files_data')
            # if files_data:
            # for file_data in files_data:
            #         try:
            #             ProjectFile.objects.create(file_name=file_data["file.name.split('.')[0]"], file_type=file_data["file_type.name.split('.')[0]"],
            #                                        file=file_data['file'], project_id=project)
            #         except:
            #             return Response({'result': '0', 'message': '创建项目成功，上传文件失败'})
            #         return Response({'result': '1', 'message': '创建成功,有文件', 'data': {}})
            return Response({'result': '1', 'message': '创建成功', 'data': {'project_id': project.id}})
        return Response({'result': '0', 'message': '数据不完整' + str(form.errors)})

    def put(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'project', 'change'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        project = Project.objects.filter(id=pk).first()
        if project and project.state != '0':
            return Response({'result': '0', 'message': '非草稿状态，无法修改', 'data': {}})
        form = SupplyLandForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            state = data['state']
            print('state', data['state'])
            project.state = data['state']
            project.name= data['name']
            project.apply_date = data['apply_date']
            project.type = data['type']
            project.used_areas = data['used_areas']
            project.covered_area = data['covered_area']
            project.plot_ratio = data['plot_ratio']
            project.project_four_to_scope = data['project_four_to_scope']
            project.project_address = data['project_address']
            project.use_land_type = data['use_land_type']
            project.investor = data['investor']

            project.project_introduction = data['project_introduction']
            project.holding_main = data['holding_main']
            project.investment_properties = data['investment_properties']
            project.registered_fund = data['registered_fund']
            project.aggregate_investment = data['aggregate_investment']
            project.estimated_sales = data['estimated_sales']
            project.estimated_tax = data['estimated_tax']
            project.contact_people = data['contact_people']
            project.contact_way = data['contact_way']
            project.docking_domain = data['docking_domain']
            if data['land_resource_ids']:
                project.land_resources.set(data['land_resource_ids'])
            if data['plant_resource_ids']:
                project.plant_resources.set(data['plant_resource_ids'])
            if data['building_resource_ids']:
                project.building_resources.set(data['building_resource_ids'])
            if data['store_resource_ids']:
                project.store_resources.set(data['store_resource_ids'])
            project.save()
            if not project.progresses.filter(user_id__isnull=False).first():
                ProjectProgress.objects.create(project_id=project, result='3', start_time=datetime.datetime.now(),
                                               user_id=user)

            if state == '1':  # 提交
                group = Group.objects.filter(name='产促中心').first()  # TODO:隐患
                ProjectProgress.objects.create(project_id=project, start_time=datetime.datetime.now(), role_id=group)
            return Response({'result': '1', 'message': '修改成功', 'data': {}})
        return Response({'result': '0', 'message': '数据不完整' + str(form.errors)})


class LeaseProjectView(APIView):
    """get:查看租赁类项目详情"""
    """post:新建租赁类项目"""
    """put:修改租赁类项目"""

    def get_object(self, pk):
        try:
            return Project.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'project', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        lease = self.get_object(pk)
        seriz = LeaseDetailSerializer(lease)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功'})

    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'project', 'add'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        form = LeaseForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            state = data['state']
            try:
                print(data)
                project = Project.objects.create(
                    user_id=user,
                    name=data['name'], state=state,
                    type=data['type'],
                    apply_date=data['apply_date'],
                    scope_business=data['scope_business'],
                    address_type=data['address_type'],
                    project_address=data['project_address'],
                    registered_fund=data['registered_fund'],
                    estimated_tax=data['estimated_tax'],
                    aggregate_investment=data['aggregate_investment'],
                    investor=data['investor'],
                    estimated_sales=data['estimated_sales'],
                    contact_people=data['contact_people'],
                    project_introduction=data['project_introduction'],
                    contact_way=data['contact_way'],
                    used_areas=data['used_areas'],
                    license_number=data['license_number'],
                    resource_owner_name=data['resource_owner_name'],
                    resource_owner_type=data['resource_owner_type'],
                    resource_transfer_name=data['resource_transfer_name'],
                    resource_transfer_type=data['resource_transfer_type'],
                    use_year=data['use_year'],
                    use_fee=data['use_fee'])

            except Exception as e:
                return Response(
                    {'result': '0', 'message': '创建失败,' + str(e) + 'state:' + data['state'] + 'type:' + data['type']})
            project.number = generate_project_number(data['type'], project.id)
            if data['land_resource_ids']:
                project.land_resources.set(data['land_resource_ids'])
            if data['plant_resource_ids']:
                project.plant_resources.set(data['plant_resource_ids'])
            if data['building_resource_ids']:
                project.building_resources.set(data['building_resource_ids'])
            if data['store_resource_ids']:
                project.store_resources.set(data['store_resource_ids'])
            project.save()
            if not project.progresses.filter(user_id__isnull=False).first():
                ProjectProgress.objects.create(project_id=project, result='3', start_time=datetime.datetime.now(),
                                               user_id=user)
            if state == '1':  # 提交
                group = Group.objects.filter(name='产促中心').first()  # TODO:隐患
                ProjectProgress.objects.create(project_id=project, start_time=datetime.datetime.now(), role_id=group)
            # files_data = request.data.get('files_data')
            # if files_data:
            #     for file_data in files_data:
            #         try:
            #             ProjectFile.objects.create(file_name=file_data["file.name.split('.')[0]"],
            #                                        file_type=file_data["file_type.name.split('.')[0]"],
            #                                        file=file_data['file'], project_id=project)
            #         except:
            #             return Response({'result': '0', 'message': '创建项目成功，上传文件失败'})
            #         return Response({'result': '1', 'message': '创建成功，有文件', 'data': {'project_record_id': project.id}})
            return Response({'result': '1', 'message': '创建成功', 'data': {'project_id': project.id}})
        return Response({'result': '0', 'message': '数据不完整' + str(form.errors)})

    def put(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'project', 'change'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        project = Project.objects.filter(id=pk).first()
        if project and project.state != '0':
            return Response({'result': '0', 'message': '非草稿状态，无法修改', 'data': {}})
        form = LeaseForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            state = data['state']
            print('state', data['state'])
            project.name = data['name']
            project.state = data['state']
            project.apply_date = data['apply_date']
            project.type = data['type']
            project.scope_business = data['scope_business']
            project.address_type = data['address_type']
            project.project_address = data['project_address']
            project.registered_fund = data['registered_fund']
            project.estimated_tax = data['estimated_tax']
            project.aggregate_investment = data['aggregate_investment']
            project.investor = data['investor']
            project.estimated_sales = data['estimated_sales']
            project.contact_people = data['contact_people']
            project.project_introduction = data['project_introduction']
            project.contact_way = data['contact_way']
            project.used_areas = data['used_areas']
            project.license_number = data['license_number']
            project.resource_owner_name = data['resource_owner_name']
            project.resource_owner_type = data['resource_owner_type']
            project.resource_transfer_name = data['resource_transfer_name']
            project.resource_transfer_type = data['resource_transfer_type']
            project.use_year = data['use_year']
            project.use_fee = data['use_fee']
            if data['land_resource_ids']:
                project.land_resources.set(data['land_resource_ids'])
            if data['plant_resource_ids']:
                project.plant_resources.set(data['plant_resource_ids'])
            if data['building_resource_ids']:
                project.building_resources.set(data['building_resource_ids'])
            if data['store_resource_ids']:
                project.store_resources.set(data['store_resource_ids'])
            project.save()
            if not project.progresses.filter(user_id__isnull=False).first():
                ProjectProgress.objects.create(project_id=project, result='3', start_time=datetime.datetime.now(),
                                               user_id=user)
            if state == '1':  # 提交
                group = Group.objects.filter(name='产促中心').first()  # TODO:隐患
                ProjectProgress.objects.create(project_id=project, start_time=datetime.datetime.now(), role_id=group)
            return Response({'result': '1', 'message': '修改成功', 'data': {}})
        return Response({'result': '0', 'data': {}, 'message': '数据不完整' + str(form.errors)})


# 删除项目
class ProjectDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Project.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def delete(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'project', 'delete'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        project = self.get_object(pk)
        project.delete()
        return Response({'result': '1', 'message': '获取成功'})


class ProjectAccessOpinionlView(APIView):
    """get：准入审批意见"""

    def get_object(self, pk):
        try:
            return Project.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'project', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        if not check_action_permission(user, 'projectprogress', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        project = self.get_object(pk)
        seriz = ProjectAccessOpinionlSerializer(project)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功'})


class ProjectApprovalView(APIView):
    """post:新建审批意见"""

    def post(self, request):
        """每个project必须有一个user_id指向创建用户的progress记录
            所以在新建项目的时候，需要为其创建progress
            若之后退回修改，应新增一条progress记录，但该记录应在审批退回修改接口中创建"""
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'projectprogress', 'add'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        project_id = request.data.get('project_id')
        if not project_id:
            return Response({'result': '0', 'data': {}, 'message': '缺少project_id'})
        project = Project.objects.filter(id=int(project_id))[0]
        print(type(project.state))
        if not project:
            return Response({'result': '0', 'data': {}, 'message': '该项目不存在'})
        # if (project.state=='1' and not user.role_id.name == '产促中心') or (project.state=='2' and not user.role_id.name==''):  # TODO
        # return Response({'result': '0', 'message': '该用户无权限'})
        progress = None
        if project.state in ['1', '3']:  # 已提交，产促办审核 or 审核部门全通过，镇长审核

            progress = project.progresses.filter(role_id=user.role_id, result__isnull=True).first()

        elif project.state == '2':  # 产促办通过，审核部门审核
            progress = project.progresses.filter(department_id=user.department_id, result__isnull=True).first()
        elif project.state == '5':  # 未通过
            return Response({'result': '0', 'data': {}, 'message': '该项目已被拒绝，无法再审批'})
        if not progress:
            return Response({'result': '0', 'data': {}, 'message': '该用户无权限'})
        opinion = request.data.get('opinion')
        if not opinion:
            return Response({'result': '0', 'data': {}, 'message': '缺少opinion'})

        result = request.data.get('result')
        # 修改对应的progress
        progress.result = result
        progress.opinion = opinion
        progress.end_time = datetime.datetime.now()
        progress.save()
        if project.state == '1':  # 产促办审批
            if result == '1':  # 同意
                department_ids = request.data.get('department_ids')
                if department_ids:
                    departments = Department.objects.filter(id__in=department_ids.split(',')).all()
                    for department in departments:
                        # TODO:可能会重复创建
                        ProjectProgress.objects.create(project_id=project, department_id=department,
                                                       start_time=datetime.datetime.now())
                    project.state='2'
                    project.save()
            elif result == '0':  # 不同意
                project.state = '5'
                project.save()
            else:  # 退回修改
                project.state = '0'
                project.save()
                ProjectProgress.objects.create(project_id=project, result='3', start_time=datetime.datetime.now(),
                                               user_id=project.user_id)

        elif project.state == '2':  # 审核部门审批，需判断其他审核部门审核情况
            if result == '1':  # 同意
                if project.progresses.filter(result__isnull=True).count() == 0:  # 若为最后一个部门
                    if project.progresses.filter(department_id__isnull=False, result='2').first():  # 是否有审核是退回修改
                        project.state = '0'
                        ProjectProgress.objects.create(project_id=project, result='3',
                                                       start_time=datetime.datetime.now(),
                                                       user_id=project.user_id)
                    else:
                        project.state = '3'
                        # 为镇长创建progress
                        group = Group.objects.filter(name='镇长').first()  # TODO:隐患
                        ProjectProgress.objects.create(project_id=project, role_id=group,
                                                       start_time=datetime.datetime.now())
                    project.save()

            elif result == '0':  # 不同意，其他审核部门无需再审核，自动赋为“未处理”#TODO
                to_do_progresses = project.progresses.filter(result__isnull=True).all()
                to_do_progresses.update(result='3')
                project.state = '5'
                project.save()
            else:  # 退回修改
                if project.progresses.filter(result__isnull=True).count() == 0:  # 若为最后一个部门
                    project.state = '0'
                    project.save()
                    ProjectProgress.objects.create(project_id=project, result='3', start_time=datetime.datetime.now(),
                                                   user_id=project.user_id)

        elif project.state == '3':  # 镇长审批，直接修改状态
            if result == '1':  # 同意
                project.state = '4'
                project.save()
            elif result == '0':  # 不同意
                project.state = '5'
                project.save()
            else:  # 退回修改
                project.state = '0'
                project.save()
                ProjectProgress.objects.create(project_id=project, result='3', start_time=datetime.datetime.now(),
                                               user_id=project.user_id)

        return Response({'result': '1', 'data': {}, 'message': '审批成功成功'})


class ProjectProgressView(APIView):
    """get:流程办理查看"""

    def get_object(self, pk):
        try:
            return Project.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if not check_action_permission(user, 'project', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        if not check_action_permission(user, 'projectprogress', 'view'):
            return Response({'result': '0', 'message': '该用户无此权限'})
        project = self.get_object(pk)
        seriz = ViewProjectProgressSerializer(project)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功'})

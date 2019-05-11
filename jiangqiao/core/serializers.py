from rest_framework import serializers
from core.models import *
from jiangqiao.settings import SERVER_MEDIA
from datetime import timedelta
from core.permission import *
import time, datetime, pytz


class LoginSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    role_name = serializers.SerializerMethodField()
    permission = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'role_name', 'department_name', 'permission')

    def get_department_name(self, obj):
        if obj.department_id:
            return obj.department_id.name
        return ''

    def get_role_name(self, obj):
        if obj.role_id:
            return obj.role_id.name
        return ''

    def get_permission(self, obj):
        return get_user_permissions(obj)


class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'type')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class UserListSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'password', 'role_name', 'department_name')

    def get_role_name(self, obj):
        if obj.role_id:
            return obj.role_id.name
        return ''

    def get_department_name(self, obj):
        if obj.department_id:
            return obj.department_id.name
        return ''


class UserDetailSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'password', 'role', 'department')

    def get_role(self, obj):
        if obj.role_id:
            return RoleSerializer(obj.role_id).data
        return ''

    def get_department(self, obj):
        if obj.department_id:
            return DepartmentListSerializer(obj.department_id).data
        return ''


class NoticeListSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = ('id', 'type', 'name', 'created_on', 'file_url', 'is_read')

    def get_file_url(self, obj):
        if obj.file:
            return SERVER_MEDIA + obj.file.name

    def get_is_read(self, obj):
        user = self.context['user']
        if user.read_records.filter(notice_id=obj).first():
            return True
        return False


class NoticeDetailSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = ('id', 'type', 'content', 'name', 'created_on', 'file_url')

    def get_file_url(self, obj):
        if obj.file:
            return SERVER_MEDIA + obj.file.name


class LandResourceListSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    related_projects = serializers.SerializerMethodField()
    residue_month = serializers.SerializerMethodField()


    class Meta:
        model = LandResource
        fields = ('id', 'location', 'state', 'ground_situation', 'land_nature', 'domicile',
                  'floor_space', 'plot_ratio', 'max_height', 'lease_month', 'vacant_area', 'residue_month',
                  'remark', 'department_name', 'user_id', 'related_projects', 'created_on')

    def get_residue_month(self, obj):
        return obj.lease_month - int((datetime.datetime.now() - obj.created_on).days / 30)

    def get_related_projects(self, obj):
        return ','.join([project.name for project in obj.project_ids.all()])


    def get_department_name(self, obj):
        return obj.user_id.get_department_name()


class LandResourceDetailSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    residue_month = serializers.SerializerMethodField()

    class Meta:
        model = LandResource
        fields = ('id', 'location', 'state', 'ground_situation', 'land_nature', 'domicile',
                  'floor_space', 'plot_ratio', 'max_height', 'lease_month', 'vacant_area', 'residue_month',
                  'remark', 'department_name', 'user_id', 'created_on')

    def get_department_name(self, obj):
        return obj.user_id.get_department_name()

    def get_residue_month(self, obj):
        return obj.lease_month - int((datetime.datetime.now() - obj.created_on).days / 30)


class PlantResourceListSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    related_projects = serializers.SerializerMethodField()
    residue_month = serializers.SerializerMethodField()

    class Meta:
        model = PlantResource
        fields = ('id', 'name', 'location', 'property', 'state', 'sewage_pipe', 'plies',
                  'floor_space', 'covered_area', 'produce_evidence', 'vacant_area', 'created_on',
                  'lease_month', 'residue_month', 'remark', 'department_name', 'user_id', 'related_projects')

    def get_related_projects(self, obj):
        return ','.join([project.name for project in obj.project_ids.all()])


    def get_department_name(self, obj):
        return obj.user_id.get_department_name()

    def get_residue_month(self, obj):
        return obj.lease_month - int((datetime.datetime.now() - obj.created_on).days / 30)


class PlantResourceDetailSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    residue_month = serializers.SerializerMethodField()

    class Meta:
        model = PlantResource
        fields = ('id', 'name', 'location', 'property', 'state', 'sewage_pipe', 'plies',
                  'floor_space', 'covered_area', 'produce_evidence', 'vacant_area', 'created_on',
                  'lease_month', 'residue_month', 'remark', 'department_name', 'user_id')

    def get_department_name(self, obj):
        return obj.user_id.get_department_name()

    def get_residue_month(self, obj):
        return obj.lease_month - int((datetime.datetime.now() - obj.created_on).days / 30)


class BuildingResourceListSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    related_projects = serializers.SerializerMethodField()
    residue_month = serializers.SerializerMethodField()

    class Meta:
        model = BuildingResource
        fields = ('id', 'name', 'location', 'property', 'state',
                  'sewage_pipe', 'plies', 'floor_space', 'covered_area',
                  'vacant_area', 'produce_evidence', 'created_on',
                  'lease_month', 'residue_month', 'remark', 'department_name', 'user_id', 'related_projects')

    def get_related_projects(self, obj):
        return ','.join([project.name for project in obj.project_ids.all()])


    def get_department_name(self, obj):
        return obj.user_id.get_department_name()

    def get_residue_month(self, obj):
        return obj.lease_month - int((datetime.datetime.now() - obj.created_on).days / 30)


class BuildingResourceDetailSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    residue_month = serializers.SerializerMethodField()

    class Meta:
        model = BuildingResource
        fields = ('id', 'name', 'location', 'property', 'state',
                  'sewage_pipe', 'plies', 'floor_space', 'covered_area',
                  'vacant_area', 'produce_evidence', 'created_on',
                  'lease_month', 'residue_month', 'remark', 'department_name', 'user_id')

    def get_department_name(self, obj):
        return obj.user_id.get_department_name()

    def get_residue_month(self, obj):
        return obj.lease_month - int((datetime.datetime.now() - obj.created_on).days / 30)


class StoreResourceListSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    related_projects = serializers.SerializerMethodField()
    residue_month = serializers.SerializerMethodField()

    class Meta:
        model = StoreResource
        fields = ('id', 'name', 'location', 'state', 'plies', 'total_area',
                  'produce_evidence', 'vacant_area', 'sewage_pipe', 'created_on',
                  'lease_month', 'residue_month', 'remark', 'department_name', 'user_id', 'related_projects')

    def get_related_projects(self, obj):
        return ','.join([project.name for project in obj.project_ids.all()])


    def get_department_name(self, obj):
        return obj.user_id.get_department_name()

    def get_residue_month(self, obj):
        return obj.lease_month - int((datetime.datetime.now() - obj.created_on).days / 30)


class StoreResourceDetailSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    residue_month = serializers.SerializerMethodField()

    class Meta:
        model = StoreResource
        fields = ('id', 'name', 'location', 'state', 'plies', 'total_area',
                  'produce_evidence', 'vacant_area', 'sewage_pipe', 'created_on',
                  'lease_month', 'residue_month', 'remark', 'department_name', 'user_id')


    def get_department_name(self, obj):
        return obj.user_id.get_department_name()

    def get_residue_month(self, obj):
        return obj.lease_month - int((datetime.datetime.now() - obj.created_on).days / 30)


class ProjectFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectFile
        fields = ('id', 'file_name', 'file_type', 'file_url', 'created_on')

    def get_file_url(self, obj):
        if obj.file:
            return SERVER_MEDIA + obj.file.name


class SupplyLandDetailSerializer(serializers.ModelSerializer):
    land_resources = serializers.SerializerMethodField()
    plant_resources = serializers.SerializerMethodField()
    building_resources = serializers.SerializerMethodField()
    store_resources = serializers.SerializerMethodField()
    project_files = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'name', 'number', 'type', 'state', 'apply_date', 'used_areas', 'covered_area', 'plot_ratio',
            'project_address', 'use_land_type', 'investor', 'project_introduction', 'holding_main',
            'investment_properties', 'registered_fund', 'aggregate_investment', 'estimated_sales',
            'estimated_tax', 'contact_people', 'contact_way', 'docking_domain', 'project_four_to_scope',
            'land_resources', 'plant_resources', 'building_resources', 'store_resources', 'project_files')

    def get_land_resources(self, obj):
        land_resources = obj.land_resources.all()
        data = [{'id': resource.id, 'name': resource.location} for resource in land_resources]
        return data

    def get_plant_resources(self, obj):
        plant_resources = obj.plant_resources.all()
        data = [{'id': resource.id, 'name': resource.name} for resource in plant_resources]
        return data

    def get_building_resources(self, obj):
        building_resources = obj.building_resources.all()
        data = [{'id': resource.id, 'name': resource.name} for resource in building_resources]
        return data

    def get_store_resources(self, obj):
        store_resources = obj.store_resources.all()
        data = [{'id': resource.id, 'name': resource.name} for resource in store_resources]
        return data

    def get_project_files(self, obj):
        all_file_types = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
                          '18', '19', '20']
        result = []
        file_types = list(set(obj.files.all().values_list('file_type', flat=True)))
        for file_type in all_file_types:
            if file_type in file_types:
                result.append({'type': file_type,
                               'list': ProjectFileSerializer(obj.files.filter(file_type=file_type), many=True).data})
            else:
                result.append({'type': file_type,
                               'list': []})
        return result


class LeaseDetailSerializer(serializers.ModelSerializer):
    land_resources = serializers.SerializerMethodField()
    plant_resources = serializers.SerializerMethodField()
    building_resources = serializers.SerializerMethodField()
    store_resources = serializers.SerializerMethodField()
    project_files = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('name', 'number', 'apply_date', 'type', 'project_address', 'address_type', 'project_four_to_scope',
                  'investor', 'registered_fund', 'estimated_sales', 'estimated_tax', 'aggregate_investment',
                  'scope_business', 'contact_people', 'contact_way', 'project_introduction',
                  'used_areas', 'license_number', 'resource_owner_name', 'resource_owner_type',
                  'resource_transfer_name', 'resource_transfer_type', 'use_year', 'use_fee', 'state',
                  'land_resources', 'plant_resources', 'building_resources', 'store_resources', 'project_files')

    def get_land_resources(self, obj):
        land_resources = obj.land_resources.all()
        data = [{'id': resource.id, 'name': resource.location} for resource in land_resources]
        return data

    def get_plant_resources(self, obj):
        plant_resources = obj.plant_resources.all()
        data = [{'id': resource.id, 'name': resource.name} for resource in plant_resources]
        return data

    def get_building_resources(self, obj):
        building_resources = obj.building_resources.all()
        data = [{'id': resource.id, 'name': resource.name} for resource in building_resources]
        return data

    def get_store_resources(self, obj):
        store_resources = obj.store_resources.all()
        data = [{'id': resource.id, 'name': resource.name} for resource in store_resources]
        return data

    def get_project_files(self, obj):
        all_file_types = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
                          '18', '19', '20']
        result = []
        file_types = list(set(obj.files.all().values_list('file_type', flat=True)))
        for file_type in all_file_types:
            if file_type in file_types:
                result.append({'type': file_type,
                               'list': ProjectFileSerializer(obj.files.filter(file_type=file_type), many=True).data})
            else:
                result.append({'type': file_type,
                               'list': []})
        return result


class ProjectListSerializer(serializers.ModelSerializer):
    # department = Department.objects.filter()
    land_resources = serializers.SerializerMethodField()
    plant_resources = serializers.SerializerMethodField()
    building_resources = serializers.SerializerMethodField()
    store_resources = serializers.SerializerMethodField()
    state_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'number', 'apply_date', 'type', 'project_four_to_scope',
                  'project_address', 'address_type', 'investor', 'registered_fund', 'estimated_sales',
                  'estimated_tax', 'scope_business', 'aggregate_investment',
                  'contact_people', 'contact_way', 'project_introduction', 'used_areas',
                  'license_number', 'resource_owner_name', 'resource_owner_type',
                  'resource_transfer_name', 'state', 'state_name', 'resource_transfer_type',
                  'covered_area', 'use_land_type', 'plot_ratio',
                  'holding_main', 'investment_properties', 'use_year', 'use_fee', 'docking_domain',
                  'land_resources', 'store_resources', 'plant_resources', 'building_resources',
        )

    def get_land_resources(self, obj):
        data = ','.join([resource.location for resource in obj.land_resources.all()])
        return data

    def get_plant_resources(self, obj):
        return ','.join([resource.name for resource in obj.plant_resources.all()])

    def get_building_resources(self, obj):
        return ','.join([resource.name for resource in obj.building_resources.all()])

    def get_store_resources(self, obj):
        return ','.join([resource.name for resource in obj.store_resources.all()])

    def get_state_name(self, obj):
        if obj.state == '0' and obj.progresses.count() > 0:
            return '退回修改'
        else:
            return obj.get_state_display()


class AdmissionApplyInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'project_address', 'department_name', 'investment_main')


class ProjectProgressSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    handle_days = serializers.SerializerMethodField()
    node_status = serializers.SerializerMethodField()
    remark = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = ProjectProgress
        fields = (
            'id', 'department_name', 'start_time', 'end_time', 'handle_days', 'result', 'node_status', 'opinion',
            'remark', 'title')

    def get_department_name(self, obj):
        if obj.department_id:
            return obj.department_id.name
        else:
            return ''

    def get_handle_days(self, obj):  # TODO:根据工作日计算
        if obj.end_time and obj.start_time:
            handle_days = (obj.end_time - obj.start_time).days
        else:
            handle_days = (datetime.datetime.now() - obj.start_time).days
        return handle_days

    def get_node_status(self, obj):  # TODO:区间
        handle_days = self.get_handle_days(obj)
        if handle_days < 3:  # 绿灯
            return '1'
        elif handle_days >= 3 or handle_days < 5:  # 黄灯
            return '2'
        else:
            return '3'

    def get_remark(self, obj):  # TODO:
        if obj.department_id and obj.end_time:
            return obj.department_id.name + '于' + str(obj.end_time)[:19] + obj.get_result_display()
        elif obj.department_id:
            return obj.department_id.name + '未处理'
        elif obj.role_id and obj.role_id.name == '产促中心' and obj.result == '1':
            return '产促中心于' + str(obj.end_time)[:19] + '提请各科室意见'
        elif obj.role_id and obj.role_id.name == '产促中心':
            return '产促中心于' + str(obj.end_time)[:19] + '不通过'
        elif obj.role_id and obj.role_id.name == '镇长':
            return '镇长于' + str(obj.end_time)[:19] + obj.get_result_display()
        elif obj.user_id:
            return obj.user_id.name + '于' + str(obj.end_time)[:19] + '数据填报完成'
        return obj.department_id.name + '于' + obj.end_time + obj.result

    def get_title(self, obj):  # TODO
        if obj.user_id:
            return '数据填报'
        elif obj.role_id and obj.role_id.name == '产促中心':
            return '产促中心办理'
        elif obj.role_id and obj.role_id.name == '镇长':
            return '领导审阅'
        elif obj.department_id:
            return '审核部门'
        return ''


class SimpleProjectProgressSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = ProjectProgress
        fields = ('id', 'opinion', 'title')

    def get_title(self, obj):  # TODO
        if obj.user_id:
            return '数据填报'
        elif obj.role_id and obj.role_id.name == '产促中心':
            return '产促中心意见'
        elif obj.role_id and obj.role_id.name == '镇长':
            return '领导意见'
        elif obj.department_id:
            return obj.department_id.name + '意见'
        return ''


class ViewProjectProgressSerializer(serializers.ModelSerializer):
    progresses = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('name', 'project_address', 'investor', 'type', 'progresses')

    def get_progresses(self, obj):
        seriz = ProjectProgressSerializer(obj.progresses, many=True)
        return seriz.data


class ProjectAccessOpinionlSerializer(serializers.ModelSerializer):
    progresses = serializers.SerializerMethodField()
    project_name = serializers.CharField(source='name')

    class Meta:
        model = Project
        fields = ('id', 'name', 'project_name', 'project_address', 'used_areas', 'estimated_tax', 'estimated_sales',
                  'docking_domain', 'use_year', 'progresses')

    def get_progresses(self, obj):
        seriz = SimpleProjectProgressSerializer(obj.progresses, many=True)
        return seriz.data


class MessageSerializer(serializers.ModelSerializer):
    yellow_count = serializers.SerializerMethodField()
    green_count = serializers.SerializerMethodField()
    red_count = serializers.SerializerMethodField()
    unread_notice_count = serializers.SerializerMethodField()
    approved_count = serializers.SerializerMethodField()
    rejected_count = serializers.SerializerMethodField()
    to_be_approval_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('yellow_count', 'green_count', 'red_count', 'unread_notice_count', 'approved_count', 'rejected_count',
                  'to_be_approval_count')

    def get_yellow_count(self, obj):
        progresses = obj.get_yellow_progresses()
        if progresses:
            return progresses.count()
        return 0

    def get_green_count(self, obj):
        progresses = obj.get_green_progresses()
        if progresses:
            return progresses.count()
        return 0

    def get_red_count(self, obj):
        progresses = obj.get_red_progresses()
        if progresses:
            return progresses.count()
        return 0

    def get_unread_notice_count(self, obj):  # TODO:
        """所有账户都需要该值"""
        """未读的新通知条数"""
        notice_count = Notice.objects.count()
        read_count = obj.read_records.count()
        return notice_count - read_count

    def get_approved_count(self, obj):
        """村级账户才需要该值"""
        """该用户的获批项目条数"""
        if obj.is_village_department():
            if obj.department_id:
                count = Project.objects.filter(user_id__department_id=obj.department_id, state='4').count()
                return count
        return 0


    def get_rejected_count(self, obj):
        """村级账户才需要该值"""
        """该用户的否决项目条数"""
        if obj.is_village_department():
            if obj.department_id:
                count = Project.objects.filter(user_id__department_id=obj.department_id, state='5').count()
                return count
        return 0


    def get_to_be_approval_count(self, obj):
        """镇长及产促中心账户才需要该值"""
        """该用户的待审项目条数"""
        if obj.is_mayor() or obj.is_center():
            count = ProjectProgress.objects.filter(role_id=obj.role_id, project_id__state__in=['1', '2', '3'],
                                                   result__isnull=True).count()
            return count
        return 0



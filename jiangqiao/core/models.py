from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from django.db.models import Q


class User(AbstractUser):
    name = models.CharField('姓名', max_length=16, null=True)
    role_id = models.ForeignKey(to=Group, verbose_name='角色', related_name='role_users', on_delete=models.SET_NULL,
                                null=True, blank=True)
    department_id = models.ForeignKey('Department', verbose_name='部门', related_name='users', on_delete=models.SET_NULL,
                                      null=True, blank=True)

    class Meta:
        verbose_name_plural = '用户表'
        verbose_name = '用户'

    def __str__(self):
        return self.username

    def get_department_name(self):
        """资源、项目中，填报单位的显示"""
        if self.department_id:
            return self.department_id.name
        elif self.role_id:
            return self.role_id.name
        else:
            return '无'

    def is_mayor(self):
        """是否为镇长"""
        if self.role_id and self.role_id.name == '镇长':
            return True
        return False

    def is_center(self):
        """是否为产促中心"""
        if self.role_id and self.role_id.name == '产促中心':
            return True
        return False

    def is_town_department(self):
        """是否为镇级部门"""
        if self.department_id and self.department_id.type == '1':
            return True
        return False

    def is_village_department(self):
        """是否为村级部门"""
        if self.department_id and self.department_id.type == '2':
            return True
        return False

    def get_yellow_progresses(self):
        """镇级账户才需要该值"""
        """黄灯预警项目记录:需要该账户审批的在审项目(3-5天)的记录"""
        if self.is_town_department():
            min_time = datetime.now() - timedelta(days=5)
            max_time = datetime.now() - timedelta(days=3)
            return ProjectProgress.objects.filter(department_id=self.department_id,
                                                  project_id__state__in=['1', '2', '3'],
                                                  result__isnull=True, start_time__gte=min_time,
                                                  start_time__lte=max_time)
        return []

    def get_green_progresses(self):
        """镇级账户才需要该值"""
        """绿灯正常项目记录:需要该账户审批的在审项目小于3天的记录"""
        if self.is_town_department():
            min_time = datetime.now() - timedelta(days=3)
            return ProjectProgress.objects.filter(department_id=self.department_id,
                                                  project_id__state__in=['1', '2', '3'],
                                                  result__isnull=True, start_time__gte=min_time)
        return []

    def get_red_progresses(self):
        """镇级账户才需要该值"""
        """红灯警告项目:需要该账户审批的在审项目大于5天的记录"""
        if self.is_town_department():
            max_time = datetime.now() - timedelta(days=5)
            return ProjectProgress.objects.filter(department_id=self.department_id,
                                                  project_id__state__in=['1', '2', '3'],
                                                  result__isnull=True, start_time__lte=max_time)
        return []

    def get_trial_progresses(self):
        """需要该账户审批的在审项目"""
        if self.is_town_department():
            # 包括需要审批，和已经审批好的
            return ProjectProgress.objects.filter(Q(project_id__state__in=['2'], department_id=self.department_id,
                                                    result__isnull=True) | Q(department_id=self.department_id,
                                                                             project_id__state__in=['3', '4', '5']))

        elif self.is_mayor() or self.is_center():
            print('not is_town')
            return ProjectProgress.objects.filter(role_id=self.role_id, project_id__state__in=['1', '3'],
                                                  result__isnull=True)
        return []

    def get_progresses(self):
        """该账户审批的项目,用于资源库过滤数据"""
        if self.is_town_department():
            return ProjectProgress.objects.filter(department_id=self.department_id)
        return []


class Village(models.Model):
    name = models.CharField('村名', max_length=64)
    code = models.CharField('编码', max_length=10)

    class Meta:
        verbose_name_plural = '村庄表'
        verbose_name = '村庄'

    def __str__(self):
        return self.name + self.code


NOTICE_TYPE_CHOICE = [
    ('1', '文件'),
    ('2', '公告')
]


# 通知表
class Notice(models.Model):
    name = models.CharField('名称', max_length=128, null=True, blank=True)
    type = models.CharField(choices=NOTICE_TYPE_CHOICE, max_length=2, null=True)
    content = models.TextField('公告内容', null=True, blank=True)
    file = models.FileField('文件', upload_to='notice_files', null=True, blank=True)
    user_id = models.ForeignKey('User', verbose_name='用户', related_name='notices', on_delete=models.CASCADE, null=True,
                                blank=True)
    created_on = models.DateTimeField('发布时间 ', auto_now_add=True)

    class Meta:
        verbose_name_plural = '通知表'
        verbose_name = '通知表'

    def __str__(self):
        return self.name


class NoticeReadRecord(models.Model):
    """通知已读记录"""
    notice_id = models.ForeignKey('Notice', related_name='read_records', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', related_name='read_records', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '通知已读记录'
        verbose_name = '通知已读记录'

    def __str__(self):
        return (self.notice_id.name or '') + (self.user_id.name or '')


STATE_CHOICE = [
    ('0', '暂时保存'),
    ('1', '提交保存'),
]
GROUND_SITUATION_CHOICE = [
    ('0', '净地'),
    ('1', '农户'),
    ('2', '企业')
]

LAND_NATURE_CHOICE = [
    ('0', '空地'),
    ('1', '农用地'),
]
LAND_DOMICILE_CHOICE = [
    ('0', '195'),
    ('1', '198'),
    ('2', '104')
]


# 土地资源表
class LandResource(models.Model):
    # land_id = models.CharField('土地序号', max_length=4, null=True, blank=True, unique=True)
    created_on = models.DateTimeField('创建日期', auto_now=True, null=True, blank=True)
    location = models.TextField('土地所在地址')
    state = models.CharField('状态', choices=STATE_CHOICE, max_length=2, default='0')
    land_nature = models.CharField('土地性质', choices=LAND_NATURE_CHOICE, max_length=2, default='0')
    domicile = models.CharField('所属产业地块', choices=LAND_DOMICILE_CHOICE, max_length=2, default='0')
    ground_situation = models.CharField('地上情况', choices=GROUND_SITUATION_CHOICE, max_length=2, default='0')
    floor_space = models.FloatField('占地面积', null=True, blank=True)
    plot_ratio = models.FloatField('容积率', null=True, blank=True)
    max_height = models.FloatField('建筑限高', null=True, blank=True)
    lease_month = models.IntegerField('租赁年限/月', null=True, blank=True)
    vacant_area = models.FloatField('空置面积', null=True, blank=True)
    residue_month = models.IntegerField('剩余时限/月', null=True, blank=True)
    remark = models.TextField('备注', null=True, blank=True)
    department_id = models.ForeignKey('Department', verbose_name='填报单位', related_name='land_resources',
                                      on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.ForeignKey('User', verbose_name='用户', related_name='land_resources',
                                on_delete=models.CASCADE, null=True, blank=True)
    project_ids = models.ManyToManyField('Project', related_name='land_resources')

    class Meta:
        verbose_name_plural = '土地资源表'
        verbose_name = '土地资源表'

        # def __str__(self):
        # return '土地序号:' + str(self.id)


SEWAGE_CHOICE = [
    ('0', '无'),
    ('1', '有')
]

PRODUCE_CHOICE = [
    ('0', '无'),
    ('1', '有')
]


# 厂房资源表
class PlantResource(models.Model):
    # plant_id = models.CharField('厂房序号', max_length=4, unique=True)
    created_on = models.DateTimeField('创建日期', auto_now_add=True, null=True, blank=True)
    name = models.CharField('厂房名称', max_length=64)
    location = models.TextField('厂房地址')
    property = models.CharField('产权方', max_length=64)
    state = models.CharField('状态', max_length=2, choices=STATE_CHOICE, default='0')
    sewage_pipe = models.CharField('污水纳管', max_length=2, choices=SEWAGE_CHOICE, default='0')
    plies = models.IntegerField('层数', null=True, blank=True)
    floor_space = models.FloatField('占地面积', null=True, blank=True)
    covered_area = models.FloatField('建筑面积', null=True, blank=True)
    produce_evidence = models.CharField('产证', max_length=2, choices=PRODUCE_CHOICE, default='0')
    vacant_area = models.FloatField('闲置面积', null=True, blank=True)
    lease_month = models.IntegerField('租赁年限/月', null=True, blank=True)
    residue_month = models.IntegerField('剩余时限/月', null=True, blank=True)
    remark = models.TextField('备注', null=True, blank=True)
    department_id = models.ForeignKey('Department', verbose_name='填报单位', related_name='plant_resources',
                                      on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.ForeignKey('User', verbose_name='用户', related_name='plant_resources',
                                on_delete=models.CASCADE, null=True, blank=True)
    project_ids = models.ManyToManyField('Project', related_name='plant_resources')

    class Meta:
        verbose_name_plural = '厂房资源表'
        verbose_name = '厂房资源表'

        # def __str__(self):
        # return self.name


# 楼宇资源表
class BuildingResource(models.Model):
    # building_num = models.CharField('楼宇序号', max_length=4, null=True, blank=True, unique=True)
    created_on = models.DateTimeField('创建日期', auto_now_add=True, null=True, blank=True)
    name = models.CharField('楼宇名称', max_length=64)
    location = models.TextField('楼宇地址')
    property = models.CharField('产权方', max_length=64)
    state = models.CharField('状态', max_length=2, choices=STATE_CHOICE, default='0')
    sewage_pipe = models.CharField('污水纳管', max_length=2, choices=SEWAGE_CHOICE, default='0')
    plies = models.IntegerField('层数', null=True, blank=True)
    floor_space = models.FloatField('占地面积', null=True, blank=True)
    covered_area = models.FloatField('建筑面积', null=True, blank=True)
    vacant_area = models.FloatField('空置面积', null=True, blank=True)
    produce_evidence = models.CharField('产证', max_length=2, choices=PRODUCE_CHOICE, default='0')
    lease_month = models.IntegerField('租赁年限/月', null=True, blank=True)
    residue_month = models.IntegerField('剩余时限/月', null=True, blank=True)
    remark = models.TextField('备注', null=True, blank=True)
    department_id = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name='填报单位',
                                      related_name='building_resources', null=True, blank=True)
    user_id = models.ForeignKey('User', verbose_name='用户', related_name='building_resources',
                                on_delete=models.CASCADE, null=True, blank=True)
    project_ids = models.ManyToManyField('Project', related_name='building_resources')

    class Meta:
        verbose_name_plural = '楼宇资源表'
        verbose_name = '楼宇资源表'

        # def __str__(self):
        # return self.name


# 商铺资源表
class StoreResource(models.Model):
    # store_num = models.CharField('商铺序号', max_length=4, null=True, blank=True, unique=True)
    created_on = models.DateTimeField('创建日期', auto_now_add=True, null=True, blank=True)
    name = models.CharField('商铺名称', max_length=128, null=True, blank=True)
    location = models.TextField('商铺地址', null=True, blank=True)
    state = models.CharField('状态', max_length=2, choices=STATE_CHOICE, default='0')
    plies = models.IntegerField('层数', null=True, blank=True)
    produce_evidence = models.CharField('产证', max_length=2, choices=PRODUCE_CHOICE, default='0')
    vacant_area = models.FloatField('空置面积', null=True, blank=True)
    total_area = models.FloatField('总面积', null=True, blank=True)
    sewage_pipe = models.CharField('污水纳管', max_length=2, choices=SEWAGE_CHOICE, default='0')
    lease_month = models.IntegerField('租赁年限/月', null=True, blank=True)
    residue_month = models.IntegerField('剩余时限/月', null=True, blank=True)
    remark = models.TextField('备注', null=True, blank=True)
    department_id = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name='填报单位',
                                      related_name='store_resources', null=True, blank=True)
    user_id = models.ForeignKey('User', verbose_name='用户', related_name='store_resources',
                                on_delete=models.CASCADE, null=True, blank=True)
    project_ids = models.ManyToManyField('Project', related_name='store_resources')

    class Meta:
        verbose_name_plural = '商铺资源表'
        verbose_name = '商铺资源表'

        # def __str__(self):
        # return self.name


PROJECT_STATE_CHOICE = [
    ('0', '草稿'),
    ('1', '已提交'),
    ('2', '产促办通过'),
    ('3', '审核部通过'),
    ('4', '已通过'),
    ('5', '未通过')
]

ADDRESS_TYPE_CHOICE = [
    ('0', '新设'),
    ('1', '迁址'),
    ('2', '动迁'),
    ('3', '其他'),
]

RESOURCE_OWNER_TYPE_CHOICE = [
    ('0', '集体'),
    ('1', '私营'),
    ('2', '其他'),
]

RESOURCE_TRANSFER_TYPE_CHOICE = [
    ('0', '集体'),
    ('1', '私营'),
    ('2', '其他'),
]

USE_LAND_TYPE_CHOICE = [
    ('0', '商办用地'),
    ('1', '工业用地'),
    ('2', '研发用地'),
]

INVESTMENT_PROPERTIES_CHOICE = [
    ('0', '社会投资'),
    ('1', '国资'),
]
PROJECT_TYPE_CHOICE = [
    ('1', '一般实体产业'),
    ('2', '工业实体产业'),
    ('3', '拟出让土地'),
    ('4', '历史存量土地')
]


# 项目总库表
class Project(models.Model):
    number = models.CharField('序号', max_length=16, null=True, blank=True)
    apply_date = models.DateTimeField('申请日期', null=True, blank=True)
    name = models.CharField('项目名称', max_length=64)
    type = models.CharField('类型', max_length=2, choices=PROJECT_TYPE_CHOICE, default='0')
    project_address = models.TextField('项目地址', null=True, blank=True)
    address_type = models.CharField('地址类型', max_length=2, choices=ADDRESS_TYPE_CHOICE, default='0', null=True,
                                    blank=True)
    project_four_to_scope = models.TextField('项目四至范围', null=True, blank=True)
    investor = models.CharField('投资主体', max_length=64, null=True, blank=True)
    registered_fund = models.FloatField('注册资金', null=True, blank=True)
    estimated_sales = models.FloatField('预计销售额/达产销售额', null=True, blank=True)
    estimated_tax = models.FloatField('预计税收/达产税收', null=True, blank=True)
    aggregate_investment = models.FloatField("投资总额", null=True, blank=True)
    scope_business = models.CharField("经营范围", max_length=64, null=True, blank=True)
    contact_people = models.CharField("联系人", max_length=10, null=True, blank=True)
    contact_way = models.CharField("联系方式", max_length=11, null=True, blank=True)
    project_introduction = models.TextField("项目简介/项目建设内容", null=True, blank=True)
    used_areas = models.FloatField('使用面积', null=True, blank=True)
    license_number = models.CharField("产证编号", max_length=16, null=True, blank=True)
    resource_owner_name = models.CharField("资源所有方名称", max_length=16, null=True, blank=True)
    resource_owner_type = models.CharField('资源所有方类型', max_length=2, choices=RESOURCE_OWNER_TYPE_CHOICE, default='0',
                                           null=True, blank=True)
    resource_transfer_name = models.CharField('资源出让方名称', max_length=16, null=True, blank=True)
    resource_transfer_type = models.CharField('资源出让方类型', max_length=2, choices=RESOURCE_TRANSFER_TYPE_CHOICE,
                                              default='0', null=True, blank=True)
    use_year = models.IntegerField('意向使用年限', null=True, blank=True)
    use_fee = models.FloatField("意向使用费用", null=True, blank=True)

    covered_area = models.FloatField('建筑面积', null=True, blank=True)
    plot_ratio = models.FloatField('容积率', null=True, blank=True)
    use_land_type = models.CharField('用地类型', max_length=2, choices=USE_LAND_TYPE_CHOICE, default='0', null=True,
                                     blank=True)
    holding_main = models.CharField('拿地主体', max_length=64, null=True, blank=True)
    investment_properties = models.CharField('投资性质', max_length=2, choices=INVESTMENT_PROPERTIES_CHOICE, default='0',
                                             null=True, blank=True)
    docking_domain = models.CharField('对接经济域', max_length=64, null=True, blank=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    state = models.CharField('审批状态', max_length=2, choices=PROJECT_STATE_CHOICE, default='0')

    class Meta:
        verbose_name_plural = '项目总库表'
        verbose_name = '项目总库表'

    def __str__(self):
        return self.name


RESULT_CHOICE = [
    ('0', '不通过'),
    ('1', '通过'),
    ('2', '退回'),
    ('3', '未处理'),

]
DEPARTMENT_TYPE_CHOICE = [
    ('1', '镇级部门'),
    ('2', '村级部门')
]


class Department(models.Model):
    name = models.CharField('部门名称', max_length=16, null=True, blank=True)
    type = models.CharField('部门类型', choices=DEPARTMENT_TYPE_CHOICE, max_length=2, null=True, blank=True)
    village_id = models.ForeignKey('Village', on_delete=models.CASCADE, related_name='departments', null=True,
                                   blank=True)

    class Meta:
        verbose_name_plural = '部门表'
        verbose_name = '部门表'

    def __str__(self):
        return self.name

    def compute_store_resource_vacant_areas(self):
        """计算该部门下，商铺资源的闲置面积总和"""
        return self.store_resources.filter(state='1').aggregate(total_vacant_areas=Sum('vacant_area'))[
                   'total_vacant_areas'] or 0.0

    def compute_store_resource_used_areas(self):
        """计算该部门下，商铺资源的使用面积总和"""
        return self.compute_store_resource_total_areas() - self.compute_store_resource_vacant_areas()

    def compute_store_resource_total_areas(self):
        """计算该部门下，商铺资源的总面积总和"""
        return self.store_resources.filter(state='1').aggregate(total_used_areas=Sum('total_area'))[
                   'total_used_areas'] or 0.0

    def compute_building_resource_vacant_areas(self):
        """计算该部门下，楼宇资源的闲置面积总和"""
        return self.building_resources.filter(state='1').aggregate(total_vacant_areas=Sum('vacant_area'))[
                   'total_vacant_areas'] or 0.0

    def compute_building_resource_total_areas(self):
        """计算该部门下，楼宇资源的用地面积总和"""
        return self.building_resources.filter(state='1').aggregate(total_used_areas=Sum('floor_space'))[
                   'total_used_areas'] or 0.0

    def compute_building_resource_used_areas(self):
        """计算该部门下，楼宇资源的总面积总和"""
        return self.compute_building_resource_total_areas() - self.compute_building_resource_vacant_areas()

    def compute_plant_resource_vacant_areas(self):
        """计算该部门下，厂房资源的闲置面积总和"""
        return self.plant_resources.filter(state='1').aggregate(total_vacant_areas=Sum('vacant_area'))[
                   'total_vacant_areas'] or 0.0

    def compute_plant_resource_total_areas(self):
        """计算该部门下，厂房资源的总面积总和"""
        return self.plant_resources.filter(state='1').aggregate(total_used_areas=Sum('floor_space'))[
                   'total_used_areas'] or 0.0

    def compute_plant_resource_used_areas(self):
        """计算该部门下，厂房资源的用地面积总和"""
        return self.compute_plant_resource_total_areas() - self.compute_plant_resource_vacant_areas()

    def compute_land_resource_vacant_areas(self):
        """计算该部门下，土地资源的闲置面积总和"""
        return self.land_resources.filter(state='1').aggregate(total_vacant_areas=Sum('vacant_area'))[
                   'total_vacant_areas'] or 0.0

    def compute_land_resource_total_areas(self):
        """计算该部门下，土地资源的总面积总和"""
        return self.land_resources.filter(state='1').aggregate(total_used_areas=Sum('floor_space'))[
                   'total_used_areas'] or 0.0

    def compute_land_resource_used_areas(self):
        """计算该部门下，土地资源的用地面积总和"""
        return self.compute_land_resource_total_areas() - self.compute_land_resource_vacant_areas()

    def compute_resource_vacant_areas(self):
        """计算该部门下，所有资源的闲置面积总和"""

        return self.compute_building_resource_vacant_areas() + self.compute_land_resource_vacant_areas() \
               + self.compute_plant_resource_vacant_areas() + self.compute_store_resource_vacant_areas()


class ProjectProgress(models.Model):
    """user_id,role_id,department_id三者不会同时有值"""
    project_id = models.ForeignKey('Project', related_name='progresses', on_delete=models.CASCADE, null=True,
                                   blank=True)
    result = models.CharField('结果', choices=RESULT_CHOICE, max_length=2, null=True,
                              blank=True)  # 若该值为空，表示未处理。若值为3，表示无需处理。
    opinion = models.TextField('意见', null=True, blank=True)
    user_id = models.ForeignKey('User', related_name='progresses', on_delete=models.SET_NULL, null=True, blank=True)
    role_id = models.ForeignKey(to=Group, related_name='progresses', on_delete=models.SET_NULL, null=True, blank=True)
    department_id = models.ForeignKey('Department', related_name='progresses', verbose_name='部门',
                                      on_delete=models.SET_NULL, null=True,
                                      blank=True)
    start_time = models.DateTimeField('开始时间', null=True, blank=True)
    end_time = models.DateTimeField('结束时间', null=True, blank=True)

    class Meta:
        verbose_name_plural = '审批意见表'
        verbose_name = '审批意见表'


FILE_TYPE_CHOICE = [
    ('1', '嘉定区供地类项目准入申请表'),
    ('2', '项目单篇材料'),
    ('3', '项目可行性报告'),
    ('4', '营业执照'),
    ('5', '法人身份证'),
    ('6', '全体股东身份证或企业营业执照'),
    ('7', '租赁合同(或者租赁意向书)	'),
    ('8', '房产证'),
    ('9', '情况说明(虚拟注册型)按需提供'),
    ('10', '嘉定区产业项目(租赁厂房)准入评审申请表'),
    ('11', '项目单篇评审报告'),
    ('12', '企业营业执照'),
    ('13', '项目可行性报告(纸..)'),
    ('14', '项目可行性报告(老..)'),
    ('15', '银行资信证明(外资)'),
    ('16', '租赁合同(或者租赁意向书)PDF电子版'),
    ('17', '拟租赁的标准厂房相关资质材料电子版(消防、环评验收报告等)'),
    ('18', '厂房不同角度的实景照片(内景+外景共3张)'),
    ('19', '汇总表电子版'),
    ('20', '情况说明(虚拟注册型)'),

]


class ProjectFile(models.Model):
    file_name = models.CharField('文件名', max_length=64)
    file_type = models.CharField('文件类型', max_length=2, choices=FILE_TYPE_CHOICE)
    project_id = models.ForeignKey('Project', related_name='files', verbose_name='项目', on_delete=models.CASCADE)
    file = models.FileField('文件', upload_to='file', null=True, blank=True)
    created_on = models.DateTimeField('上传时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = '项目文件'
        verbose_name = '项目文件'

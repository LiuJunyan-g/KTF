# Generated by Django 2.1.2 on 2018-12-24 09:08

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=16, null=True, verbose_name='姓名')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户表',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BuildingResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='楼宇名称')),
                ('location', models.TextField(verbose_name='楼宇地址')),
                ('property', models.CharField(max_length=64, verbose_name='产权方')),
                ('state', models.CharField(choices=[('0', '暂时保存'), ('1', '提交保存')], default='0', max_length=2, verbose_name='状态')),
                ('sewage_pipe', models.CharField(choices=[('0', '无'), ('1', '有')], default='0', max_length=2, verbose_name='污水纳管')),
                ('plies', models.IntegerField(blank=True, null=True, verbose_name='层数')),
                ('floor_space', models.FloatField(blank=True, null=True, verbose_name='占地面积')),
                ('covered_area', models.FloatField(blank=True, null=True, verbose_name='建筑面积')),
                ('vacant_area', models.FloatField(blank=True, null=True, verbose_name='空置面积')),
                ('produce_evidence', models.CharField(choices=[('0', '无'), ('1', '有')], default='0', max_length=2, verbose_name='产证')),
                ('lease_month', models.IntegerField(blank=True, null=True, verbose_name='租赁年限/月')),
                ('residue_month', models.IntegerField(blank=True, null=True, verbose_name='剩余时限/月')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '楼宇资源表',
                'verbose_name_plural': '楼宇资源表',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=16, null=True, verbose_name='部门名称')),
                ('type', models.CharField(blank=True, choices=[('1', '镇级部门'), ('2', '村级部门')], max_length=2, null=True, verbose_name='部门类型')),
            ],
            options={
                'verbose_name': '部门表',
                'verbose_name_plural': '部门表',
            },
        ),
        migrations.CreateModel(
            name='LandResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('location', models.TextField(verbose_name='土地所在地址')),
                ('state', models.CharField(choices=[('0', '暂时保存'), ('1', '提交保存')], default='0', max_length=2, verbose_name='状态')),
                ('land_nature', models.CharField(choices=[('0', '空地'), ('1', '农用地')], default='0', max_length=2, verbose_name='土地性质')),
                ('domicile', models.CharField(choices=[('0', '195'), ('1', '198'), ('2', '104')], default='0', max_length=2, verbose_name='所属产业地块')),
                ('ground_situation', models.CharField(choices=[('0', '净地'), ('1', '农户'), ('2', '企业')], default='0', max_length=2, verbose_name='地上情况')),
                ('floor_space', models.FloatField(blank=True, null=True, verbose_name='占地面积')),
                ('plot_ratio', models.FloatField(blank=True, null=True, verbose_name='容积率')),
                ('max_height', models.FloatField(blank=True, null=True, verbose_name='建筑限高')),
                ('lease_month', models.IntegerField(blank=True, null=True, verbose_name='租赁年限/月')),
                ('vacant_area', models.FloatField(blank=True, null=True, verbose_name='空置面积')),
                ('residue_month', models.IntegerField(blank=True, null=True, verbose_name='剩余时限/月')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('department_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='land_resources', to='core.Department', verbose_name='填报单位')),
            ],
            options={
                'verbose_name': '土地资源表',
                'verbose_name_plural': '土地资源表',
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='名称')),
                ('type', models.CharField(choices=[('1', '文件'), ('2', '公告')], max_length=2, null=True)),
                ('content', models.TextField(blank=True, null=True, verbose_name='公告内容')),
                ('file', models.FileField(blank=True, null=True, upload_to='notice_files', verbose_name='文件')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='发布时间 ')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notices', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '通知表',
                'verbose_name_plural': '通知表',
            },
        ),
        migrations.CreateModel(
            name='NoticeReadRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notice_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_records', to='core.Notice')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_records', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '通知已读记录',
                'verbose_name_plural': '通知已读记录',
            },
        ),
        migrations.CreateModel(
            name='PlantResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='厂房名称')),
                ('location', models.TextField(verbose_name='厂房地址')),
                ('property', models.CharField(max_length=64, verbose_name='产权方')),
                ('state', models.CharField(choices=[('0', '暂时保存'), ('1', '提交保存')], default='0', max_length=2, verbose_name='状态')),
                ('sewage_pipe', models.CharField(choices=[('0', '无'), ('1', '有')], default='0', max_length=2, verbose_name='污水纳管')),
                ('plies', models.IntegerField(blank=True, null=True, verbose_name='层数')),
                ('floor_space', models.FloatField(blank=True, null=True, verbose_name='占地面积')),
                ('covered_area', models.FloatField(blank=True, null=True, verbose_name='建筑面积')),
                ('produce_evidence', models.CharField(choices=[('0', '无'), ('1', '有')], default='0', max_length=2, verbose_name='产证')),
                ('vacant_area', models.FloatField(blank=True, null=True, verbose_name='闲置面积')),
                ('lease_month', models.IntegerField(blank=True, null=True, verbose_name='租赁年限/月')),
                ('residue_month', models.IntegerField(blank=True, null=True, verbose_name='剩余时限/月')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('department_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plant_resources', to='core.Department', verbose_name='填报单位')),
            ],
            options={
                'verbose_name': '厂房资源表',
                'verbose_name_plural': '厂房资源表',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=16, null=True, verbose_name='序号')),
                ('apply_date', models.DateTimeField(blank=True, null=True, verbose_name='申请日期')),
                ('name', models.CharField(max_length=64, verbose_name='项目名称')),
                ('type', models.CharField(choices=[('1', '一般实体产业'), ('2', '工业实体产业'), ('3', '拟出让土地'), ('4', '历史存量土地')], default='0', max_length=2, verbose_name='类型')),
                ('project_address', models.TextField(blank=True, null=True, verbose_name='项目地址')),
                ('address_type', models.CharField(blank=True, choices=[('0', '新设'), ('1', '迁址'), ('2', '动迁'), ('3', '其他')], default='0', max_length=2, null=True, verbose_name='地址类型')),
                ('project_four_to_scope', models.TextField(blank=True, null=True, verbose_name='项目四至范围')),
                ('investor', models.CharField(blank=True, max_length=64, null=True, verbose_name='投资主体')),
                ('registered_fund', models.FloatField(blank=True, null=True, verbose_name='注册资金')),
                ('estimated_sales', models.FloatField(blank=True, null=True, verbose_name='预计销售额/达产销售额')),
                ('estimated_tax', models.FloatField(blank=True, null=True, verbose_name='预计税收/达产税收')),
                ('aggregate_investment', models.FloatField(blank=True, null=True, verbose_name='投资总额')),
                ('scope_business', models.CharField(blank=True, max_length=64, null=True, verbose_name='经营范围')),
                ('contact_people', models.CharField(blank=True, max_length=10, null=True, verbose_name='联系人')),
                ('contact_way', models.CharField(blank=True, max_length=11, null=True, verbose_name='联系方式')),
                ('project_introduction', models.TextField(blank=True, null=True, verbose_name='项目简介/项目建设内容')),
                ('used_areas', models.FloatField(blank=True, null=True, verbose_name='使用面积')),
                ('license_number', models.CharField(blank=True, max_length=16, null=True, verbose_name='产证编号')),
                ('resource_owner_name', models.CharField(blank=True, max_length=16, null=True, verbose_name='资源所有方名称')),
                ('resource_owner_type', models.CharField(blank=True, choices=[('0', '集体'), ('1', '私营'), ('2', '其他')], default='0', max_length=2, null=True, verbose_name='资源所有方类型')),
                ('resource_transfer_name', models.CharField(blank=True, max_length=16, null=True, verbose_name='资源出让方名称')),
                ('resource_transfer_type', models.CharField(blank=True, choices=[('0', '集体'), ('1', '私营'), ('2', '其他')], default='0', max_length=2, null=True, verbose_name='资源出让方类型')),
                ('use_year', models.IntegerField(blank=True, null=True, verbose_name='意向使用年限')),
                ('use_fee', models.FloatField(blank=True, null=True, verbose_name='意向使用费用')),
                ('covered_area', models.FloatField(blank=True, null=True, verbose_name='建筑面积')),
                ('plot_ratio', models.FloatField(blank=True, null=True, verbose_name='容积率')),
                ('use_land_type', models.CharField(blank=True, choices=[('0', '商办用地'), ('1', '工业用地'), ('2', '研发用地')], default='0', max_length=2, null=True, verbose_name='用地类型')),
                ('holding_main', models.CharField(blank=True, max_length=64, null=True, verbose_name='拿地主体')),
                ('investment_properties', models.CharField(blank=True, choices=[('0', '社会投资'), ('1', '国资')], default='0', max_length=2, null=True, verbose_name='投资性质')),
                ('docking_domain', models.CharField(blank=True, max_length=64, null=True, verbose_name='对接经济域')),
                ('state', models.CharField(choices=[('0', '草稿'), ('1', '已提交'), ('2', '产促办已通过'), ('3', '审核部门已通过'), ('4', '已通过'), ('5', '未通过')], default='0', max_length=2, verbose_name='审批状态')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '项目总库表',
                'verbose_name_plural': '项目总库表',
            },
        ),
        migrations.CreateModel(
            name='ProjectFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=64, verbose_name='文件名')),
                ('file_type', models.CharField(choices=[('1', '嘉定区供地类项目准入申请表'), ('2', '项目单篇材料'), ('3', '项目可行性报告'), ('4', '营业执照'), ('5', '法人身份证'), ('6', '全体股东身份证或企业营业执照'), ('7', '租赁合同(或者租赁意向书)\t'), ('8', '房产证'), ('9', '情况说明(虚拟注册型)按需提供'), ('10', '嘉定区产业项目(租赁厂房)准入评审申请表'), ('11', '项目单篇评审报告'), ('12', '企业营业执照'), ('13', '项目可行性报告(纸..)'), ('14', '项目可行性报告(老..)'), ('15', '银行资信证明(外资)'), ('16', '租赁合同(或者租赁意向书)PDF电子版'), ('17', '拟租赁的标准厂房相关资质材料电子版(消防、环评验收报告等)'), ('18', '厂房不同角度的实景照片(内景+外景共3张)'), ('19', '汇总表电子版'), ('20', '情况说明(虚拟注册型)')], max_length=2, verbose_name='文件类型')),
                ('file', models.FileField(blank=True, null=True, upload_to='file', verbose_name='文件')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='上传时间')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='core.Project', verbose_name='项目')),
            ],
            options={
                'verbose_name': '项目文件',
                'verbose_name_plural': '项目文件',
            },
        ),
        migrations.CreateModel(
            name='ProjectProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(choices=[('0', '不同意'), ('1', '同意'), ('2', '退回'), ('3', '未处理')], max_length=2, null=True, verbose_name='结果')),
                ('opinion', models.TextField(blank=True, null=True, verbose_name='意见')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='开始时间')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='结束时间')),
                ('department_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='progresses', to='core.Department', verbose_name='部门')),
                ('project_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='progresses', to='core.Project')),
                ('role_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='progresses', to='auth.Group')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='progresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '审批意见表',
                'verbose_name_plural': '审批意见表',
            },
        ),
        migrations.CreateModel(
            name='StoreResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='商铺名称')),
                ('location', models.TextField(blank=True, null=True, verbose_name='商铺地址')),
                ('state', models.CharField(choices=[('0', '暂时保存'), ('1', '提交保存')], default='0', max_length=2, verbose_name='状态')),
                ('plies', models.IntegerField(blank=True, null=True, verbose_name='层数')),
                ('produce_evidence', models.CharField(choices=[('0', '无'), ('1', '有')], default='0', max_length=2, verbose_name='产证')),
                ('vacant_area', models.FloatField(blank=True, null=True, verbose_name='空置面积')),
                ('total_area', models.FloatField(blank=True, null=True, verbose_name='总面积')),
                ('sewage_pipe', models.CharField(choices=[('0', '无'), ('1', '有')], default='0', max_length=2, verbose_name='污水纳管')),
                ('lease_month', models.IntegerField(blank=True, null=True, verbose_name='租赁年限/月')),
                ('residue_month', models.IntegerField(blank=True, null=True, verbose_name='剩余时限/月')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('department_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store_resources', to='core.Department', verbose_name='填报单位')),
                ('project_ids', models.ManyToManyField(related_name='store_resources', to='core.Project')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store_resources', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '商铺资源表',
                'verbose_name_plural': '商铺资源表',
            },
        ),
        migrations.CreateModel(
            name='Village',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='村名')),
                ('code', models.CharField(max_length=10, verbose_name='编码')),
            ],
            options={
                'verbose_name': '村庄',
                'verbose_name_plural': '村庄表',
            },
        ),
        migrations.AddField(
            model_name='plantresource',
            name='project_ids',
            field=models.ManyToManyField(related_name='plant_resources', to='core.Project'),
        ),
        migrations.AddField(
            model_name='plantresource',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plant_resources', to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='landresource',
            name='project_ids',
            field=models.ManyToManyField(related_name='land_resources', to='core.Project'),
        ),
        migrations.AddField(
            model_name='landresource',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='land_resources', to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='department',
            name='village_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='core.Village'),
        ),
        migrations.AddField(
            model_name='buildingresource',
            name='department_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='building_resources', to='core.Department', verbose_name='填报单位'),
        ),
        migrations.AddField(
            model_name='buildingresource',
            name='project_ids',
            field=models.ManyToManyField(related_name='building_resources', to='core.Project'),
        ),
        migrations.AddField(
            model_name='buildingresource',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='building_resources', to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='user',
            name='department_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='core.Department', verbose_name='部门'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='role_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='role_users', to='auth.Group', verbose_name='角色'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]

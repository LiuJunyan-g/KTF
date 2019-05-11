from . import views
from django.urls import path
from core.views import *
from core.resource_index import *
from core.notice import *
from core.land_resource import *
from core.plant_resource import *
from core.building_resource import *
from core.store_resource import *
from core.project import *
from core.login import *
from core.privilege_management import *
from core.project_file import *
from core.index import *
from core.project_index import *

app_name = 'jiangqiao'

urlpatterns = [
    # 登录
    path('login/', LoginView.as_view()),
    # 首页
    path('index/', IndexView.as_view()),
    # 修改密码
    path('change_password/', ChangePassword.as_view()),
    # 获取账户列表
    path('get_users/', UserView.as_view()),
    # 新建账户
    path('create_user/', UserView.as_view()),
    # 查看账户详情
    path('get_user_detail/<int:pk>/', UserDetailView.as_view()),
    # 修改账户信息
    path('update_user/<int:pk>/', UserView.as_view()),
    # 删除账户信息
    path('delete_user/<int:pk>/', UserView.as_view()),
    # 查看部门列表
    path('get_departments/', DepartmentView.as_view()),
    # 新建部门
    path('create_department/', DepartmentView.as_view()),
    # 修改部门名称
    path('update_department/<int:pk>/', DepartmentView.as_view()),
    # 删除部门
    path('delete_department/<int:pk>/', DepartmentView.as_view()),
    # 查看角色列表
    path('get_roles/', RoleView.as_view()),

    # 上传文件:用于对已存在的项目进行文件上传
    path('create_project_file/', ProjectFileView.as_view()),
    # 删除文件
    path('delete_project_file/<int:pk>/', ProjectFileDeleteView.as_view()),


    # 获取村庄列表

    # 获取通知列表
    path('get_notices/', NoticeListView.as_view()),
    # 新建通知
    path('create_notice/', NoticeListView.as_view()),
    # 查看通知详情
    path('get_notice_detail/<int:pk>/', NoticeDetailView.as_view()),
    # 删除通知
    path('delete_notice/<int:pk>/', NoticeDeleteView.as_view()),
    # 资源库首页
    path('get_resource_index_data/', ResourceIndexView.as_view()),
    # 项目库首页
    path('get_approval_index_data/', ProjectIndexView.as_view()),

    # 获取土地资源列表
    path('get_land_resources/', LandResourceListView.as_view()),
    # 新建土地资源
    path('create_land_resource/', LandResourceListView.as_view()),
    # 查看土地资源详情
    path('get_land_resource_detail/<int:pk>/', LandResourceDetailView.as_view()),
    # 修改土地资源详情
    path('update_land_resource/<int:pk>/', LandResourceDetailView.as_view()),
    # 删除勾选的土地资源
    path('delete_land_resource/<int:pk>/', LandResourceDeleteView.as_view()),


    # 获取厂房资源列表
    path('get_plant_resources/', PlantResourceListView.as_view()),
    # 新建厂房资源
    path('create_plant_resource/', PlantResourceListView.as_view()),
    # 查看厂房资源详情
    path('get_plant_resource_detail/<int:pk>/', PlantResourceDetailView.as_view()),
    # 修改厂房资源详情
    path('update_plant_resource/<int:pk>/', PlantResourceDetailView.as_view()),
    # 删除勾选的厂房资源
    path('delete_plant_resource/<int:pk>/', PlantResourceDeleteView.as_view()),


    # 获取楼宇资源列表
    path('get_building_resources/', BuildingResourceListView.as_view()),
    # 新建楼宇资源
    path('create_building_resource/', BuildingResourceListView.as_view()),
    # 查看楼宇资源详情
    path('get_building_resource_detail/<int:pk>/', BuildingResourceDetailView.as_view()),
    # 修改楼宇资源详情
    path('update_building_resource/<int:pk>/', BuildingResourceDetailView.as_view()),
    # 删除勾选的楼宇资源
    path('delete_building_resource/<int:pk>/', BuildingResourceDeleteView.as_view()),

    # 获取商铺资源列表
    path('get_store_resources/', StoreResourceListView.as_view()),
    # 新建商铺资源
    path('create_store_resource/', StoreResourceListView.as_view()),
    # 查看商铺资源详情
    path('get_store_resource_detail/<int:pk>/', StoreResourceDetailView.as_view()),
    # 修改商铺资源详情
    path('update_store_resource/<int:pk>/', StoreResourceDetailView.as_view()),
    # 删除勾选的商铺资源
    path('delete_store_resource/<int:pk>/', StoreResourceDeleteView.as_view()),


    # 项目列表
    path('get_projects/', ProjectListView.as_view()),
    # 删除项目
    path('delete_project/<int:pk>/', ProjectDeleteView.as_view()),

    # 新建供地类项目
    path('create_project_supply_land/', SupplyLandProjectView.as_view()),
    # 修改供地类项目
    path('update_project_supply_land/<int:pk>/', SupplyLandProjectView.as_view()),
    # 查看详情
    path('get_project_supply_land_detail/<int:pk>/', SupplyLandProjectView.as_view()),

    # 新建租赁项目
    path('create_project_lease/', LeaseProjectView().as_view()),
    # 修改租赁项目
    path('update_project_lease/<int:pk>/', LeaseProjectView.as_view()),
    # 查看详情
    path('get_project_lease_detail/<int:pk>/', LeaseProjectView.as_view()),

    # 审批
    path('approval_project/', ProjectApprovalView.as_view()),
    # 流程办理查看
    path('get_project_progresses/<int:pk>/', ProjectProgressView.as_view()),
    # 查看审批意见
    path('get_project_access_opinion/<int:pk>/', ProjectAccessOpinionlView.as_view()),

    # 获取项目序号
    path('get_project_generate_number/', ProjectView.as_view()),


    path('get_messages/', MessageView.as_view())


]

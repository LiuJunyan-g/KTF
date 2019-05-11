from django.contrib import admin
from core.models import *


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'role_id', 'department_id')


@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'content', 'name', 'created_on', 'file', 'user_id')


@admin.register(NoticeReadRecord)
class NoticeReadRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'notice_id')


@admin.register(LandResource)
class LandResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'state', 'ground_situation', 'land_nature', 'domicile', 'vacant_area',
                    'floor_space', 'plot_ratio', 'max_height', 'lease_month', 'residue_month',
                    'remark', 'department_id', 'user_id', 'created_on')
    fields = ('location', 'state', 'ground_situation', 'land_nature', 'domicile', 'vacant_area',
              'floor_space', 'plot_ratio', 'max_height', 'lease_month', 'residue_month',
              'remark', 'department_id', 'user_id', 'project_ids')


@admin.register(PlantResource)
class PlantResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'property', 'state', 'sewage_pipe', 'plies',
                    'floor_space', 'covered_area', 'produce_evidence', 'created_on',
                    'lease_month', 'residue_month', 'remark', 'department_id', 'user_id')
    fields = ('name', 'location', 'property', 'state', 'sewage_pipe', 'plies',
              'floor_space', 'covered_area', 'produce_evidence',
              'lease_month', 'residue_month', 'remark', 'department_id', 'user_id', 'project_ids')


@admin.register(BuildingResource)
class BuildingResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'property', 'state',
                    'sewage_pipe', 'plies', 'floor_space', 'covered_area',
                    'vacant_area', 'produce_evidence',
                    'lease_month', 'residue_month', 'remark', 'department_id', 'user_id', 'created_on')
    fields = ('name', 'location', 'property', 'state',
              'sewage_pipe', 'plies', 'floor_space', 'covered_area',
              'vacant_area', 'produce_evidence',
              'lease_month', 'residue_month', 'remark', 'department_id', 'user_id', 'project_ids')


@admin.register(StoreResource)
class StoreResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'state', 'plies', 'total_area',
                    'produce_evidence', 'vacant_area', 'sewage_pipe',
                    'lease_month', 'residue_month', 'remark', 'department_id', 'user_id', 'created_on')
    fields = ('name', 'location', 'state', 'plies', 'total_area',
              'produce_evidence', 'vacant_area', 'sewage_pipe',
              'lease_month', 'residue_month', 'remark', 'department_id', 'user_id', 'project_ids')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number', 'apply_date', 'type', 'project_four_to_scope',
                    'project_address', 'address_type', 'investor', 'registered_fund', 'estimated_sales',
                    'estimated_tax', 'scope_business', 'aggregate_investment',
                    'contact_people', 'contact_way', 'project_introduction', 'used_areas',
                    'license_number', 'resource_owner_name', 'resource_owner_type',
                    'resource_transfer_name', 'state', 'resource_transfer_type',
                    'covered_area', 'use_land_type', 'plot_ratio',
                    'holding_main', 'investment_properties', 'use_year', 'use_fee', 'docking_domain', 'user_id')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'village_id')


@admin.register(ProjectProgress)
class ProjectProgressAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'project_id', 'result', 'opinion', 'user_id', 'role_id', 'department_id', 'start_time', 'end_time')
@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'file_type', 'project_id', 'created_on', 'file')
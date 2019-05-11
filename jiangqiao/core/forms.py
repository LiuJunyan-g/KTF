from django import forms
from core.models import *
# from django.forms import ModelForm


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','name','role_id', 'password')


class LandResourceForm(forms.ModelForm):
    # projects = forms.ModelMultipleChoiceField(Project.objects.all(), required=False)

    class Meta:
        model = LandResource
        fields = ('location', 'state', 'ground_situation', 'land_nature', 'domicile',
                  'floor_space', 'plot_ratio', 'max_height', 'lease_month', 'vacant_area', 'residue_month',
                  'remark')


class PlantResourceForm(forms.ModelForm):
    # project_id = forms.ModelMultipleChoiceField(Project.objects.all(), required=False)
    class Meta:
        model = PlantResource
        fields = ('name', 'location', 'property', 'state', 'sewage_pipe', 'plies',
                  'floor_space', 'covered_area', 'produce_evidence', 'vacant_area',
                  'lease_month', 'residue_month', 'remark')


class BuildingResourceForm(forms.ModelForm):
    # project_id = forms.ModelMultipleChoiceField(Project.objects.all(), required=False)
    class Meta:
        model = BuildingResource
        fields = ('name', 'location', 'property', 'state',
                  'sewage_pipe', 'plies', 'floor_space', 'covered_area',
                  'vacant_area', 'produce_evidence',
                  'lease_month', 'residue_month', 'remark')


class StoreResourceForm(forms.ModelForm):
    # project_id = forms.ModelMultipleChoiceField(Project.objects.all(), required=False)

    class Meta:
        model = StoreResource
        fields = ('name', 'location', 'state', 'plies', 'total_area',
                  'produce_evidence', 'vacant_area', 'sewage_pipe',
                  'lease_month', 'residue_month', 'remark')


# class TotalProjectForm(forms.ModelForm):
# class Meta:
# model = Project
# fields = ('number','apply_date', 'name', 'type', 'approval', 'address',
# 'address_type', 'register_money', 'expect_money', 'expect_tax', 'investment_money',
#                   'scope_business', 'contact_people', 'contact_mobile', 'intro',
#                   'resource_area', 'license_number', 'source', 'use_year', 'use_fee')


class SupplyLandForm(forms.ModelForm):
    land_resource_ids = forms.CharField(required=False)
    plant_resource_ids = forms.CharField(required=False)
    building_resource_ids = forms.CharField(required=False)
    store_resource_ids = forms.CharField(required=False)
    apply_date = forms.CharField(required=True)


    class Meta:
        model = Project
        fields = (
            'name', 'type', 'state', 'apply_date', 'used_areas', 'covered_area', 'plot_ratio', 'project_four_to_scope',
            'project_address', 'use_land_type', 'investor', 'project_introduction', 'holding_main',
            'investment_properties', 'registered_fund', 'aggregate_investment', 'estimated_sales',
            'estimated_tax', 'contact_people', 'contact_way', 'docking_domain',
            'land_resource_ids', 'plant_resource_ids', 'building_resource_ids', 'store_resource_ids',)

    def clean_apply_date(self):
        return str(self.cleaned_data['apply_date'])[:19].replace('T',' ')

    def clean_land_resource_ids(self):
        land_resource_ids = self.cleaned_data['land_resource_ids']
        if land_resource_ids:
            return LandResource.objects.filter(id__in=land_resource_ids.split(',')).all()
        else:
            return None

    def clean_plant_resource_ids(self):
        plant_resource_ids = self.cleaned_data['plant_resource_ids']
        if plant_resource_ids:
            return PlantResource.objects.filter(id__in=plant_resource_ids.split(',')).all()
        else:
            return None
    def clean_building_resource_ids(self):
        building_resource_ids = self.cleaned_data['building_resource_ids']
        if building_resource_ids:
            return BuildingResource.objects.filter(id__in=building_resource_ids.split(',')).all()
        else:
            return None

    def clean_store_resource_ids(self):
        store_resource_ids = self.cleaned_data['store_resource_ids']
        if store_resource_ids:
            return StoreResource.objects.filter(id__in=store_resource_ids.split(',')).all()
        else:
            return None


class LeaseForm(forms.ModelForm):
    land_resource_ids = forms.CharField(required=False)
    plant_resource_ids = forms.CharField(required=False)
    building_resource_ids = forms.CharField(required=False)
    store_resource_ids = forms.CharField(required=False)
    apply_date = forms.CharField(required=True)

    class Meta:
        model = Project
        fields = ('name', 'apply_date', 'type', 'project_address', 'address_type', 'project_four_to_scope',
                  'investor', 'registered_fund', 'estimated_sales', 'estimated_tax', 'aggregate_investment',
                  'scope_business', 'contact_people', 'contact_way', 'project_introduction',
                  'used_areas', 'license_number', 'resource_owner_name', 'resource_owner_type',
                  'resource_transfer_name', 'resource_transfer_type', 'use_year', 'use_fee', 'state',
                  'land_resource_ids', 'plant_resource_ids', 'building_resource_ids', 'store_resource_ids',)

    def clean_apply_date(self):
        return str(self.cleaned_data['apply_date'])[:19].replace('T',' ')

    def clean_land_resource_ids(self):
        land_resource_ids = self.cleaned_data['land_resource_ids']
        if land_resource_ids:
            return LandResource.objects.filter(id__in=land_resource_ids.split(',')).all()
        else:
            return None

    def clean_plant_resource_ids(self):
        plant_resource_ids = self.cleaned_data['plant_resource_ids']
        if plant_resource_ids:
            return PlantResource.objects.filter(id__in=plant_resource_ids.split(',')).all()
        else:
            return None
    def clean_building_resource_ids(self):
        building_resource_ids = self.cleaned_data['building_resource_ids']
        if building_resource_ids:
            return BuildingResource.objects.filter(id__in=building_resource_ids.split(',')).all()
        else:
            return None

    def clean_store_resource_ids(self):
        store_resource_ids = self.cleaned_data['store_resource_ids']
        if store_resource_ids:
            return StoreResource.objects.filter(id__in=store_resource_ids.split(',')).all()
        else:
            return None

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'number', 'apply_date', 'type', 'project_four_to_scope',
                  'project_address', 'address_type', 'investor', 'registered_fund', 'estimated_sales',
                  'estimated_tax', 'scope_business', 'aggregate_investment',
                  'contact_people', 'contact_way', 'project_introduction', 'used_areas',
                  'license_number', 'resource_owner_name', 'resource_owner_type',
                  'resource_transfer_name', 'state', 'resource_transfer_type',
                  'covered_area', 'use_land_type', 'plot_ratio',
                  'holding_main', 'investment_properties', 'use_year', 'use_fee', 'docking_domain')

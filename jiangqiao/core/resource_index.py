from core.serializers import *
from rest_framework.views import APIView, Response
from core.models import *


class ResourceIndexView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        analyse_data = []
        if user.role_id and user.role_id.name in ['镇长', '产促中心', '镇级部门']:

            departments = Department.objects.all()
        elif user.role_id and user.role_id.name == '村级部门':
            departments = [user.department_id]
        else:
            return Response({'result': '0', 'message': '有误'})
        type = request.GET.get('type')
        if type == '1':
            for department in departments:
                analyse_data.append({'name': department.name,
                                     'unused_areas': department.compute_land_resource_vacant_areas(),
                                     'used_areas': department.compute_land_resource_used_areas(),
                                     'areas': department.compute_land_resource_total_areas()
                                     })
        elif type == '2':
            for department in departments:
                analyse_data.append({'name': department.name,
                                     'unused_areas': department.compute_plant_resource_vacant_areas(),
                                     'used_areas': department.compute_plant_resource_used_areas(),
                                     'areas': department.compute_plant_resource_total_areas()
                                     })
        elif type == '3':
            for department in departments:
                analyse_data.append({'name': department.name,
                                     'unused_areas': department.compute_building_resource_vacant_areas(),
                                     'used_areas': department.compute_building_resource_used_areas(),
                                     'areas': department.compute_building_resource_total_areas()
                                     })
        elif type == '4':
            for department in departments:
                analyse_data.append({'name': department.name,
                                     'unused_areas': department.compute_store_resource_vacant_areas(),
                                     'used_areas': department.compute_store_resource_used_areas(),
                                     'areas': department.compute_store_resource_total_areas()
                                     })
        land_unused_areas = \
        LandResource.objects.filter(department_id__in=departments).aggregate(total_vacant_areas=Sum('vacant_area'))[
            'total_vacant_areas'] or 0.0
        land_total_areas = \
        LandResource.objects.filter(department_id__in=departments).aggregate(total_used_areas=Sum('floor_space'))[
            'total_used_areas'] or 0.0

        plant_unused_areas = \
        PlantResource.objects.filter(department_id__in=departments).aggregate(total_vacant_areas=Sum('vacant_area'))[
            'total_vacant_areas'] or 0.0
        plant_total_areas = \
        PlantResource.objects.filter(department_id__in=departments).aggregate(total_used_areas=Sum('floor_space'))[
            'total_used_areas'] or 0.0

        building_unused_areas = \
        BuildingResource.objects.filter(department_id__in=departments).aggregate(total_vacant_areas=Sum('vacant_area'))[
            'total_vacant_areas'] or 0.0
        building_total_areas = \
        BuildingResource.objects.filter(department_id__in=departments).aggregate(total_used_areas=Sum('floor_space'))[
                'total_used_areas'] or 0.0

        store_unused_areas = \
        StoreResource.objects.filter(department_id__in=departments).aggregate(total_vacant_areas=Sum('vacant_area'))[
            'total_vacant_areas'] or 0.0
        store_total_areas = \
        StoreResource.objects.filter(department_id__in=departments).aggregate(total_used_areas=Sum('total_area'))[
            'total_used_areas'] or 0.0
        return Response({"data": {'analyse_data': analyse_data,
                                  "land_total_areas": land_total_areas,
                                  "land_unused_areas": land_unused_areas,
                                  "plant_total_areas": plant_total_areas,
                                  "plant_unused_areas": plant_unused_areas,
                                  "building_total_areas": building_total_areas,
                                  "building_unused_areas": building_unused_areas,
                                  "store_total_areas": store_total_areas,
                                  "store_unused_areas": store_unused_areas}})
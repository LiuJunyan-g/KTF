from rest_framework.views import APIView, Response
from core.models import *


class IndexView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})
        if user.is_mayor() or user.is_center() or user.is_town_department():
            project_count = Project.objects.count()
            land_resource_count = LandResource.objects.count()
            building_resource_count = BuildingResource.objects.count()
            plant_resource_count = PlantResource.objects.count()
            store_resource_count = StoreResource.objects.count()
            data = [{'project_count': project_count,
                     'land_resource_count': land_resource_count,
                     'plant_resource_count': plant_resource_count,
                     'building_resource_count': building_resource_count,
                     'store_resource_count': store_resource_count,
                    }]
            villages = Village.objects.all()
            for village in villages:
                project_count = Project.objects.filter(
                    user_id__department_id__village_id=village).count()
                land_resource_count = LandResource.objects.filter(
                    user_id__department_id__village_id=village).count()
                building_resource_count = BuildingResource.objects.filter(
                    user_id__department_id__village_id=village).count()
                plant_resource_count = PlantResource.objects.filter(
                    user_id__department_id__village_id=village).count()
                store_resource_count = StoreResource.objects.filter(
                    user_id__department_id__village_id=village).count()
                data.append({'village_code': village.code,
                             'project_count': project_count,
                             'land_resource_count': land_resource_count,
                             'plant_resource_count': plant_resource_count,
                             'building_resource_count': building_resource_count,
                             'store_resource_count': store_resource_count,
                })
        elif user.is_village_department():
            if user.department_id.village_id:
                project_count = Project.objects.filter(
                    user_id__department_id__village_id=user.department_id.village_id).count()
            else:
                project_count = Project.objects.filter(
                    user_id__department_id=user.department_id).count()
            land_resource_count = user.department_id.land_resources.count()
            plant_resource_count = user.department_id.plant_resources.count()
            building_resource_count = user.department_id.building_resources.count()
            store_resource_count = user.department_id.store_resources.count()
            data = {'village_code': '',  # 可以不要
                    'project_count': project_count,
                    'land_resource_count': land_resource_count,
                    'plant_resource_count': plant_resource_count,
                    'building_resource_count': building_resource_count,
                    'store_resource_count': store_resource_count,
            }
        else:
            return Response({'data': {}, 'result': '0', 'message': '获取失败'})
        return Response({'data': data, 'result': '1', 'message': '获取成功'})





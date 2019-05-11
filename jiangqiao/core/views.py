from rest_framework.views import APIView, Response
from core.serializers import *
from core.models import *
from django.contrib.auth.models import Group, Permission


PROJECT_TYPE_CHOICE = [
    ('1', '一般实体产业'),
    ('2', '工业实体产业'),
    ('3', '拟出让土地'),
    ('4', '历史存量土地')
]


def generate_project_number(project_type, object_id=None):
    length = 5
    pre_str = ''
    if project_type == '1':
        pre_str = 'JQYB-'
    elif project_type == '2':
        pre_str = 'JQGY-'
    elif project_type == '3':
        pre_str = 'JQNCR-'
    elif project_type == '4':
        pre_str = 'JQLSCL-'
    if object_id:
        # 插入数据库时
        number = pre_str + str(object_id).zfill(length)
    else:
        # 生成序号给前端时
        last_obj = Project.objects.order_by('id').last()
        if last_obj:
            number = pre_str + str(last_obj.id + 1).zfill(length)
        else:
            number = pre_str + '1'.zfill(length)

    return number


class MessageView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'result': '0', 'message': '缺少user_id'})
        user = User.objects.filter(id=int(user_id)).first()
        if not user:
            return Response({'result': '0', 'message': '该用户不存在'})

        seriz = MessageSerializer(user)
        return Response({'data': seriz.data, 'result': '1', 'message': '获取成功'})


class InitDataView(APIView):
    """用于初始化数据"""

    def get(self, request):
        village_data = [{'village_name': '高潮村', 'code': 'gaochao'},
                        {'village_name': '封浜村', 'code': 'fengbang'},
                        {'village_name': '红光村', 'code': 'hongguang'},
                        {'village_name': '华庄村', 'code': 'huazhuang'},
                        {'village_name': '火线村', 'code': 'huoxian'},
                        {'village_name': '太平村', 'code': 'taiping'},
                        {'village_name': '星火村', 'code': 'xinghuo'},
                        {'village_name': '先农村', 'code': 'xiannong'},
                        {'village_name': '江丰社区', 'code': 'jiangfeng'},
                        {'village_name': '新江村', 'code': 'xinjiang'},
                        {'village_name': '新华村', 'code': 'xinhua'},
                        {'village_name': '五四村', 'code': 'wusi'},
                        {'village_name': '幸福村', 'code': 'xingfu'},
                        {'village_name': '沙河村', 'code': 'shahe'},
                        {'village_name': '增建村', 'code': 'zengjian'},
                        {'village_name': '年丰村', 'code': 'nianfeng'},
                        {'village_name': '建华村', 'code': 'jianhua'}, ]

        for v_data in village_data:
            if not Village.objects.filter(code=v_data['code']).first():
                Village.objects.create(name=v_data['village_name'], code=v_data['code'])

        group_permission_data = [
            {'group_name': '镇长', 'permissions': [
                {'name': 'village', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'department', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'user', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'project', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'projectprogress', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'projectfile', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'landresource', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'plantresource', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'buildingresource', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'storeresource', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'notice', 'action': ['view', 'add', 'change','delete']},
            ]},

            {'group_name': '产促中心', 'permissions': [
                {'name': 'village', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'department', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'user', 'action': ['view', 'add', 'change']},
                {'name': 'project', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'projectprogress', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'projectfile', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'landresource', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'plantresource', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'buildingresource', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'storeresource', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'notice', 'action': ['view', 'add', 'change','delete']},
            ]},
            {'group_name': '镇级部门', 'permissions': [
                {'name': 'project', 'action': ['view']},
                {'name': 'projectprogress', 'action': ['view']},
                {'name': 'projectfile', 'action': ['view']},
                {'name': 'landresource', 'action': ['view']},
                {'name': 'plantresource', 'action': ['view']},
                {'name': 'buildingresource', 'action': ['view']},
                {'name': 'storeresource', 'action': ['view']},
                {'name': 'notice', 'action': ['view']},
            ]},

            {'group_name': '村级部门', 'permissions': [
                {'name': 'project', 'action': ['view', 'add', 'change']},
                {'name': 'projectprogress', 'action': ['view', 'add', 'change']},
                {'name': 'projectfile', 'action': ['view', 'add', 'change']},
                {'name': 'landresource', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'plantresource', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'buildingresource', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'storeresource', 'action': ['view', 'add', 'change', 'delete']},
                {'name': 'notice', 'action': ['view']},
            ]}
        ]
        for group_data in group_permission_data:
            group=Group.objects.filter(name=group_data['group_name']).first()
            if not group:
                group = Group.objects.create(name=group_data['group_name'])
                for model_data in group_data['permissions']:
                    for action in model_data['action']:
                        print(action + '_' + model_data['name'])
                        permission = Permission.objects.get(codename=action + '_' + model_data['name'])
                        group.permissions.add(permission)

        return Response({'result': '初始化成功'})
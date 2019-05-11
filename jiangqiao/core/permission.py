# encoding:utf-8
from django.contrib.auth.models import Permission

app = 'prm_core'


def check_action_permission(user, model='', action=''):
    """
    判断User对Model是否有action权限
    action可选值:add,change,view,delete
    """
    if not user:
        return False
    condition = {
        'codename': action + '_' + model
    }
    if user.role_id:
        model_permission = Permission.objects.filter(group=user.role_id, **condition).first()
        if model_permission:
            return True
    return False


def get_user_permissions(user):
    """
    获取用户所有登陆后所需权限的数据
    """
    permission = {'notice': {'is_create': False, 'is_retrieve': False, 'is_update': False, 'is_delete': False},
                  'resource': {'is_create': False, 'is_retrieve': False, 'is_update': False, 'is_delete': False},
                  'project': {
                      'total': {'is_create': False, 'is_retrieve': False, 'is_update': False, 'is_delete': False,
                                'is_update_progress': False, 'is_view_progress': False, 'is_view_result': False},
                      'trial': {'is_create': False, 'is_retrieve': False, 'is_update': False, 'is_delete': False,
                                'is_update_progress': False, 'is_view_progress': False, 'is_view_result': False},
                      'approved': {'is_create': False, 'is_retrieve': False, 'is_update': False, 'is_delete': False,
                                   'is_update_progress': False, 'is_view_progress': False, 'is_view_result': False},
                      'rejected': {'is_create': False, 'is_retrieve': False, 'is_update': False, 'is_delete': False,
                                   'is_update_progress': False, 'is_view_progress': False, 'is_view_result': False},
                  },

    }

    for notice_permission in permission['notice'].keys():
        if notice_permission == 'is_create':
            if check_action_permission(user, 'notice', 'add'):
                permission['notice'][notice_permission] = True
        elif notice_permission == 'is_retrieve':
            if check_action_permission(user, 'notice', 'view'):
                permission['notice'][notice_permission] = True
        elif notice_permission == 'is_update':
            if check_action_permission(user, 'notice', 'change'):
                permission['notice'][notice_permission] = True
        elif notice_permission == 'is_delete':
            if check_action_permission(user, 'notice', 'delete'):
                permission['notice'][notice_permission] = True

    for resource_permission in permission['resource'].keys():
        if resource_permission == 'is_create':
            if check_action_permission(user, 'landresource', 'add'):  # TODO:隐患
                permission['resource'][resource_permission] = True
        elif resource_permission == 'is_retrieve':
            if check_action_permission(user, 'landresource', 'view'):  # TODO:隐患
                permission['resource'][resource_permission] = True
        elif resource_permission == 'is_update':
            if check_action_permission(user, 'landresource', 'change'):  # TODO:隐患
                permission['resource'][resource_permission] = True
        elif resource_permission == 'is_delete':
            if check_action_permission(user, 'landresource', 'delete'):  # TODO:隐患
                permission['resource'][resource_permission] = True

    for project_permission in permission['project'].keys():
        for action in ['is_create', 'is_retrieve', 'is_update', 'is_delete', 'is_update_progress', 'is_view_progress',
                       'is_view_result']:
            if action == 'is_create':
                if check_action_permission(user, 'project', 'add'):
                    permission['project'][project_permission][action] = True
            elif action == 'is_retrieve':
                if check_action_permission(user, 'project', 'view'):
                    permission['project'][project_permission][action] = True
            elif action == 'is_update':
                if check_action_permission(user, 'project', 'change'):
                    permission['project'][project_permission][action] = True
            elif action == 'is_delete':
                if check_action_permission(user, 'project', 'delete'):
                    permission['project'][project_permission][action] = True
            elif action == 'is_update_progress':
                if user.is_mayor() or user.is_center() or user.is_town_department():
                    permission['project'][project_permission][action] = True
            elif action == 'is_view_progress':
                permission['project'][project_permission][action] = True
            elif action == 'is_view_result':
                permission['project'][project_permission][action] = True
    if user.is_mayor():
        permission['manage'] = {
            'user': {'is_create': False, 'is_retrieve': False, 'is_update': False, 'is_delete': False},
            'department': {'is_create': False, 'is_retrieve': False, 'is_update': False, 'is_delete': False}}
        for manage_permission in permission['manage'].keys():
            for action in ['is_create', 'is_retrieve', 'is_update', 'is_delete']:
                if action == 'is_create':
                    if check_action_permission(user, manage_permission, 'add'):
                        permission['manage'][manage_permission][action] = True
                elif action == 'is_retrieve':
                    if check_action_permission(user, manage_permission, 'view'):
                        permission['manage'][manage_permission][action] = True
                elif action == 'is_update':
                    if check_action_permission(user, manage_permission, 'change'):
                        permission['manage'][manage_permission][action] = True
                elif action == 'is_delete':
                    if check_action_permission(user, manage_permission, 'delete'):
                        permission['manage'][manage_permission][action] = True
    return permission

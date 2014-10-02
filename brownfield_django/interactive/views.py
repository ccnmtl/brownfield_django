# from django.shortcuts import render
# @jsonify.when('isinstance(obj, Group)')
# def jsonify_group(obj):
#     result = jsonify_sqlobject( obj )
#     result["users"] = [u.user_name for u in obj.users]
#     result["permissions"] = [p.permission_name for p in obj.permissions]
#     return result
#
# @jsonify.when('isinstance(obj, User)')
# def jsonify_user(obj):
#     result = jsonify_sqlobject( obj )
#     del result['password']
#     result["groups"] = [g.group_name for g in obj.groups]
#     result["permissions"] = [p.permission_name for p in obj.permissions]
#     return result
#
# @jsonify.when('isinstance(obj, Permission)')
# def jsonify_permission(obj):
#     result = jsonify_sqlobject( obj )
#     result["groups"] = [g.group_name for g in obj.groups]
#     return result

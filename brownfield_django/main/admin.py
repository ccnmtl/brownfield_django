from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from brownfield_django.main.models import UserProfile, \
    Course, Document, Team, History, PerformedTest, Information


# from pagetree.models import Hierarchy
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    list_display = ['user', 'role']


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['course', 'name', 'link', 'visible']


class PerformedTestInline(admin.TabularInline):
    model = PerformedTest


class InformationInline(admin.TabularInline):
    model = Information


class HistoryInline(admin.TabularInline):
    model = History
    inlines = [
        PerformedTestInline,
        InformationInline
    ]


class TeamAdmin(admin.ModelAdmin):
    model = Team
    search_fields = ['user__username']
    inlines = [
        HistoryInline
    ]


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Team, TeamAdmin)

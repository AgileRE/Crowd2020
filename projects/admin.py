from django.contrib import admin
from .models import Category, Project, Requirement, ProjectView, Profile, Asset, Comment, RequirementView


def approve_requirement(modeladmin,request,queryset):
    queryset.update(status='A')

def decline_requirement(modeladmin,request,queryset):
    queryset.update(status='D')

class RequirementAdmin(admin.ModelAdmin):
    list_display = ('user','timestamp','project','status','category',)
    actions=[approve_requirement, decline_requirement]
    search_fields = ('user__username', 'timestamp','project__title')
    # readonly_fields=('user', 'timestamp','content','project','category','choose',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    def has_add_permission(self, request):
        return False

        
class AssetAdmin(admin.ModelAdmin):
    list_display = ('image',)
    search_fields = ('image',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Category)
admin.site.register(Project)
admin.site.register(Profile)
admin.site.register(Asset, AssetAdmin)
admin.site.register(Requirement, RequirementAdmin)
admin.site.register(Comment)

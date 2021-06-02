from django.contrib import admin
from .models import Check, User

from django.contrib.auth.models import Group
admin.site.unregister(Group)

# Register your models here.
class CheckAdmin(admin.ModelAdmin):
    list_display = ["user", "time", "status"]
    list_display_links = list_display
    search_fields = list_display


admin.site.register(Check, CheckAdmin)


def fully_delete_selected_photos(modeladmin, request, queryset):
    from . import face_task
    queryset.delete()
    face_task.known_face_names, face_task.known_face_encodings  =face_task.load_all_users()


fully_delete_selected_photos.short_description = "删除选中"


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "pro","clss","snum","college"]
    list_display_links = ["username", "pro","clss","snum","college"]
    search_fields = list_display
    actions = [fully_delete_selected_photos, ]



    def get_actions(self, request):
        actions = super(UserAdmin, self).get_actions(request)
        print(request, actions)
        del actions['delete_selected']
        return actions


admin.site.register(User, UserAdmin)

from django.contrib import admin





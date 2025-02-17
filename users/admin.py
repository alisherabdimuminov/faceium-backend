from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


from .models import (
    Area,
    Branch,
    Control,
    Department,
    History,
    User,
    WorkingTime,
    Organization,
    Question,
    Test,
    Set,
)


@admin.register(Set)
class SetModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", ]


@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "correct_answer", "score"]
    search_fields = ["question"]

@admin.register(Test)
class TestModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "user", "set", "questions_count", "status"]
    search_fields = ["name",]


@admin.register(Organization)
class OrganizationModelAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "max_users", "count_users", "created", ]


@admin.register(Area)
class AreaModelAdmin(admin.ModelAdmin):
    list_display = ["org", "name", "alphax", "alphay", "betax", "betay", "gammax", "gammay", "deltax", "deltay", ]
    search_fields = ["name"]
    list_filter = ["org"]


@admin.register(Branch)
class BranchModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", ]


@admin.register(Control)
class ControlModelAdmin(admin.ModelAdmin):
    list_display = ["employee", "input_status", "output_status", "created", ]


@admin.register(Department)
class DepartmentModelAdmin(admin.ModelAdmin):
    list_display = ["org", "name", "created", "updated", ]
    list_filter = ["org"]


@admin.register(History)
class HistoryModelAdmin(admin.ModelAdmin):
    list_display = ["user", "model", "comment", ]


@admin.register(WorkingTime)
class WorkingTimeModelAdmin(admin.ModelAdmin):
    list_display = ["org", "name", "start", "end"]
    list_filter = ["org"]


@admin.register(User)
class UserModelAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ["org", "username", "first_name", "last_name", "middle_name", "department", "position", "working_time", ]
    search_fields = ["username", "first_name", "last_name", "middle_name", ]
    list_filter = ["org", "department", "working_time"]
    model = User
    fieldsets = (
        ("Ma'lumotlar", {
            "fields": ("uuid", "username", "first_name", "last_name", "middle_name", "password", "gender", "birth_date", "image", )
        }), 
        ("Ish va yashash joyi", {
            "fields": ("org", "branch", "department", "position", "working_time", "country", "city", "town", "address", "phone", )
        })
    )
    add_fieldsets = (
        ("Yangi foydalanuvchi qo'shish", {
            "fields": ("username", "password1", "password2", "first_name", "last_name", "middle_name", )
        }), 
        ("Ish va yashash joyi", {
            "fields": ("org", "branch", "department", "position", "working_time", "country", "city", "town", "address", "phone", )
        })
    )

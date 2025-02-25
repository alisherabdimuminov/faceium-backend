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
    Question,
    Test,
    Set,
    Task,
    Submit,
)



@admin.register(Task)
class TaskModelAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "created", "updated", ]
    search_fields = ["name", ]
    list_filter = ["user", ]


@admin.register(Submit)
class SubmitModelAdmin(admin.ModelAdmin):
    list_display = ["task", "user", "created", "updated", "status", ]
    search_fields = ["task", "user", ]
    list_filter = ["status", ]


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

@admin.register(Area)
class AreaModelAdmin(admin.ModelAdmin):
    list_display = ["name", "coord1", "coord2", "coord3", "coord4", "coord5", "coord6", "coord7", "coord8", ]
    search_fields = ["name"]


@admin.register(Branch)
class BranchModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", ]


@admin.register(Control)
class ControlModelAdmin(admin.ModelAdmin):
    list_display = ["employee", "input_status", "output_status", "created", ]


@admin.register(Department)
class DepartmentModelAdmin(admin.ModelAdmin):
    list_display = ["name", "created", "updated", ]


@admin.register(History)
class HistoryModelAdmin(admin.ModelAdmin):
    list_display = ["user", "model", "comment", ]


@admin.register(WorkingTime)
class WorkingTimeModelAdmin(admin.ModelAdmin):
    list_display = ["name", "start", "end"]


@admin.register(User)
class UserModelAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ["username", "full_name", "department", "position", "working_time", ]
    search_fields = ["username", "first_name", "last_name", "middle_name", ]
    list_filter = ["department", "working_time"]
    model = User
    fieldsets = (
        ("Ma'lumotlar", {
            "fields": ("uuid", "username", "full_name", "role", "password", "gender", "birth_date", "image", )
        }), 
        ("Ish va yashash joyi", {
            "fields": ("branch", "department", "position", "working_time", "country", "city", "town", "address", "phone", )
        })
    )
    add_fieldsets = (
        ("Yangi foydalanuvchi qo'shish", {
            "fields": ("username", "role", "password1", "password2", "full_name", )
        }), 
        ("Ish va yashash joyi", {
            "fields": ("branch", "department", "position", "working_time", "country", "city", "town", "address", "phone", )
        })
    )

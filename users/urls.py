from django.urls import path

from .views.api import check_location, check_handle, check_face
from .views.auth import login, profile
from .views.admin import (
    get_stats,
    get_users,
    add_user,
    edit_user,
    get_user,

    get_branches,
    add_branch,

    get_departments,
    add_department,
    edit_department,
    
    get_working_times,
    add_working_time,
    
    get_areas,

    get_reports,
    get_report,

    get_tests,
    add_test,

    get_sets,
    add_set,

    get_applications,
    add_application,
    get_my_applications,
)
from .views.head import (
    get_employees,
)


urlpatterns = [
    path("auth/login/", login,),
    path("auth/profile/", profile,),

    path("location/", check_location,),
    path("handle/", check_handle,),
    path("faceid/", check_face,),

    path("stats/", get_stats,),

    path("areas/", get_areas,),
    
    path("users/", get_users,),
    path("users/add/", add_user, ),
    path("users/<str:uuid>/", get_user, ),
    path("users/<str:uuid>/edit/", edit_user, ),

    path("employees/<int:pk>/", get_employees,),

    path("branches/", get_branches,),
    path("branches/add/", add_branch, ),

    path("departments/", get_departments,),
    path("departments/add/", add_department,),
    path("departments/<int:pk>/edit/", edit_department,),

    path("working_times/", get_working_times,),
    path("working_times/add/", add_working_time,),

    path("reports/", get_reports, ),
    path("reports/<str:bid>/<str:did>/", get_report, ),

    path("tests/", get_tests, ),
    path("tests/add/", add_test, ),

    path("sets/", get_sets, ),
    path("sets/add", add_set, ),

    path("tasks/", get_applications, ),
    path("tasks/add/", add_application, ),
    path("tasks/my/", get_my_applications, ),
]

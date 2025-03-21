from rest_framework import serializers

from .models import (
    User,
    Area,
    Branch,
    WorkingTime, 
    Department,
    Control,
    Question,
    Test,
    Set,
    Application,
    Submit,
)


class SetSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = Set
        fields = ("id", "name")


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("question", "answer_a", "answer_b", "answer_c", "andwer_d", "correct_answer", "score", )


class AreaSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = Area
        fields = ("id", "name", "coord1", "coord2", "coord3", "coord4", "coord5", "coord6", "coord7", "coord8", )


class WorkingTimeSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = WorkingTime
        fields = ("id", "name", "start", "end", )


class BranchSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = Branch
        fields = ("id", "name", )


class DepartmentSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    employees = serializers.SerializerMethodField("count_employees")

    def count_employees(self, obj: Department):
        employees = User.objects.filter(department=obj, is_active=True)
        return employees.count()

    class Meta:
        model = Department
        fields = ("id", "name", "employees", )


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    branch = BranchSerializer(Branch)
    department = DepartmentSerializer(Department)
    working_time = WorkingTimeSerializer(WorkingTime)
    class Meta:
        model = User
        fields = ("id", "uuid", "username", "full_name",  
                  "role", "branch", "department", "position", "gender", "working_time",
                  "birth_date", "image", "country", "city", "town", "address", "phone")


class AddUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "full_name", "role",
                  "branch", "department", "position", "gender", "working_time",
                  "birth_date", "image", "country", "city", "town", "address", "phone")    


class TestSerializer(serializers.ModelSerializer):
    user = UserSerializer(User)
    set = SetSerializer(Set)
    class Meta:
        model = Test
        fields = ("name", "user", "set", "questions_count", "passing_score", "start", "end", "duration", "status", )


class AddTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ("name", "user", "set", "passing_score", "duration", "status", )


class ControlsSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(Branch)
    department = DepartmentSerializer(Department)
    input_status = serializers.SerializerMethodField("input_status_func")
    input_area = serializers.SerializerMethodField("input_area_func")
    input_time = serializers.SerializerMethodField("input_time_func")
    output_status = serializers.SerializerMethodField("output_status_func")
    output_area = serializers.SerializerMethodField("output_area_func")
    output_time = serializers.SerializerMethodField("output_time_func")

    def input_status_func(self, obj):
        day = self.context.get("day")
        month = self.context.get("month")
        year = self.context.get("year")
        control = Control.objects.filter(employee=obj, created__day=day, created__month=month, created__year=year)
        if control.exists():
            control = control.last()
            return control.input_status
        return "didnotcome"
    
    def input_time_func(self, obj):
        day = self.context.get("day")
        month = self.context.get("month")
        year = self.context.get("year")
        control = Control.objects.filter(employee=obj, created__day=day, created__month=month, created__year=year)
        if control.exists():
            control = control.last()
            return control.input_time.strftime("%H:%M:%S") if control.input_time else None
        return None
    
    def input_area_func(self, obj):
        day = self.context.get("day")
        month = self.context.get("month")
        year = self.context.get("year")
        control = Control.objects.filter(employee=obj, created__day=day, created__month=month, created__year=year)
        if control.exists():
            control = control.last()
            return control.input_area.name if control.input_area else None
        return None
    
    def output_status_func(self, obj):
        day = self.context.get("day")
        month = self.context.get("month")
        year = self.context.get("year")
        control = Control.objects.filter(employee=obj, created__day=day, created__month=month, created__year=year)
        if control.exists():
            control = control.last()
            return control.output_status
        return "didnotcome"
    
    def output_time_func(self, obj):
        day = self.context.get("day")
        month = self.context.get("month")
        year = self.context.get("year")
        control = Control.objects.filter(employee=obj, created__day=day, created__month=month, created__year=year)
        if control.exists():
            control = control.last()
            return control.output_time.strftime("%H:%M:%S") if control.output_time else None
        return None
    
    def output_area_func(self, obj):
        day = self.context.get("day")
        month = self.context.get("month")
        year = self.context.get("year")
        control = Control.objects.filter(employee=obj, created__day=day, created__month=month, created__year=year)
        if control.exists():
            control = control.last()
            return control.output_area.name if control.output_area else None
        return None
    
    class Meta:
        model = User
        fields = ("username", "full_name", "branch", "department", "input_status", "input_area", "input_time", "output_status", "output_area", "output_time", )


class ApplicationSerializer(serializers.ModelSerializer):
    user = UserSerializer(User)
    status = serializers.SerializerMethodField("status_func")
    submit = serializers.SerializerMethodField("submit_func")

    def status_func(self, obj):
        submits = Submit.objects.filter(application=obj)
        if submits.exists():
            submit = submits.last()
            return submit.status
        return "notsubmitted"
    
    def submit_func(self, obj):
        submits = Submit.objects.filter(application=obj)
        if submits.exists():
            submit = submits.last()
            return submit.file.url
        return None

    class Meta:
        model = Application
        fields = ("id", "user", "number", "output_number", "short_description", "description", "type", "sender", "status", "submit", "entered", "exited", "executed", )


class SubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submit
        fields = ("application", "user", "file", "created", "updated", "status", )

from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager


ROLE = (
    ("admin", "Admin"),
    ("employee", "Xodim"),
    ("head", "Boshliq"),
)

GENDER = (
    ("male", "Erkak"),
    ("female", "Ayol"),
)

INPUT_STATUS = (
    ("created", "Yaratilgan"),
    ("arrived", "Kelgan"),
    ("late", "Kech qolgan"),
    ("crash", "Xatolik"),
    ("failed", "Muvaffaqiyatsiz"),
)

OUTPUT_STATUS = (
    ("created", "Yaratilgan"),
    ("gone", "Ketgan"),
    ("crash", "Xatolik"),
    ("failed", "Muvaffaqiyatisz"),
)
    

class Organization(models.Model):
    uuid = models.CharField(max_length=100, default=uuid4, editable=False)
    name = models.CharField(max_length=1000)
    description = models.TextField(null=True, blank=True)
    max_users = models.IntegerField(default=10)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def count_users(self):
        return User.objects.filter(org=self).count()

    def __str__(self):
        return self.name
    

class Branch(models.Model):
    uuid = models.CharField(max_length=100, default=uuid4, editable=False)
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Department(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tashkiloti")
    name = models.CharField(max_length=1000, verbose_name="Nomi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")
    updated = models.DateTimeField(auto_now=True, verbose_name="Tahrirlangan vaqti")

    def __str__(self):
        return self.name
   

class WorkingTime(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tashkiloti")
    name = models.CharField(max_length=1000, verbose_name="Nomi")
    start = models.TimeField(max_length=1000, verbose_name="Ish boshlanish vaqti")
    end = models.TimeField(max_length=1000, verbose_name="Ish tugash vaqti")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")
    updated = models.DateTimeField(auto_now=True, verbose_name="Tahrirlangan vaqti")

    def __str__(self):
        return f"{self.name}({self.start}-{self.end})"
    

class Set(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Question(models.Model):
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    question = models.TextField()
    answer_a = models.TextField()
    answer_b = models.TextField()
    answer_c = models.TextField()
    answer_d = models.TextField()
    correct_answer = models.CharField(max_length=10, choices=(("a", "A"), ("b", "B"), ("c", "C"), ("d", "D")))
    score = models.IntegerField(default=2)

    def __str__(self):
        return self.question


class Area(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tashkiloti")
    name = models.CharField(max_length=100, verbose_name="Nomi")
    alphax = models.DecimalField(max_digits=10, decimal_places=6)
    alphay = models.DecimalField(max_digits=10, decimal_places=6)
    betax = models.DecimalField(max_digits=10, decimal_places=6)
    betay = models.DecimalField(max_digits=10, decimal_places=6)
    gammax = models.DecimalField(max_digits=10, decimal_places=6)
    gammay = models.DecimalField(max_digits=10, decimal_places=6)
    deltax = models.DecimalField(max_digits=10, decimal_places=6)
    deltay = models.DecimalField(max_digits=10, decimal_places=6)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    uuid = models.CharField(max_length=100, default=uuid4)
    username = models.CharField(max_length=100, unique=True, verbose_name="Foydalanuvchi nomi")
    first_name = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Ismi")
    last_name = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Familiyasi")
    middle_name = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Sharifi")
    role = models.CharField(max_length=20, choices=ROLE, verbose_name="Roli")

    org = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tashkiloti")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bo'limi")
    position = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Lavozimo")
    gender = models.CharField(max_length=100, choices=GENDER, null=True, blank=True, verbose_name="Jinsi")
    working_time = models.ForeignKey(WorkingTime, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ish vaqti")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan kuni")
    image = models.ImageField(upload_to="images/users", null=True, blank=True, verbose_name="Rasmi")

    country = models.CharField(max_length=100, null=True, blank=True, verbose_name="Davlati")
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="Viloyati")
    town = models.CharField(max_length=100, null=True, blank=True, verbose_name="Tumani")
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name="Manzili")
    phone = models.CharField(max_length=100, null=True, blank=True, verbose_name="Telefon raqami")

    is_active = models.BooleanField(default=True, verbose_name="Faol")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")
    updated = models.DateTimeField(auto_now=True, verbose_name="Tahrirlangan vaqti")

    objects = UserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username


class Test(models.Model):
    uuid = models.CharField(max_length=100, default=uuid4)
    name = models.CharField(max_length=100)
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    questions_count = models.IntegerField(default=30)
    questions = models.ManyToManyField(Question, related_name="test_questions", blank=True)
    passing_score = models.IntegerField(default=50)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(default=0)
    status = models.CharField(max_length=100, choices=(("not_started", "Boshlanmagan"), ("started", "Boshlangan"), ("ended", "Tugagan"), ("passed", "O'tgan"), ("failed", "Yiqilgan")), default="created")

    def __str__(self):
        return self.name


class Control(models.Model):
    uuid = models.CharField(max_length=100, default=uuid4, editable=False)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    input_area = models.ForeignKey(Area, related_name="control_input_area", on_delete=models.SET_NULL, null=True, blank=True)
    output_area = models.ForeignKey(Area, related_name="control_output_area", on_delete=models.SET_NULL, null=True, blank=True)
    input_status = models.CharField(max_length=100, choices=INPUT_STATUS, null=True, blank=True, default="created")
    output_status = models.CharField(max_length=100, choices=OUTPUT_STATUS, null=True, blank=True, default="created")
    input_image = models.ImageField(upload_to="images/controls/input", null=True, blank=True)
    output_image = models.ImageField(upload_to="images/controls/output", null=True, blank=True)
    input_time = models.TimeField(null=True, blank=True)
    output_time = models.TimeField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.input_status


class Holiday(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="Tashkiloti")
    name = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Vocation(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField()

    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    model = models.CharField(max_length=1000)
    comment = models.CharField(max_length=1000)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.model


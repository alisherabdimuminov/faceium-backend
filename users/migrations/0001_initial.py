# Generated by Django 5.1.5 on 2025-02-24 09:00

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nomi')),
                ('coord1', models.DecimalField(decimal_places=6, max_digits=10)),
                ('coord2', models.DecimalField(decimal_places=6, max_digits=10)),
                ('coord3', models.DecimalField(decimal_places=6, max_digits=10)),
                ('coord4', models.DecimalField(decimal_places=6, max_digits=10)),
                ('coord5', models.DecimalField(decimal_places=6, max_digits=10)),
                ('coord6', models.DecimalField(decimal_places=6, max_digits=10)),
                ('coord7', models.DecimalField(decimal_places=6, max_digits=10)),
                ('coord8', models.DecimalField(decimal_places=6, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=100)),
                ('name', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, verbose_name='Nomi')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faol')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Tahrirlangan vaqti')),
            ],
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='WorkingTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, verbose_name='Nomi')),
                ('start', models.TimeField(max_length=1000, verbose_name='Ish boshlanish vaqti')),
                ('end', models.TimeField(max_length=1000, verbose_name='Ish tugash vaqti')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faol')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Tahrirlangan vaqti')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('uuid', models.CharField(default=uuid.uuid4, max_length=100)),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='Foydalanuvchi nomi')),
                ('first_name', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Ismi')),
                ('last_name', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Familiyasi')),
                ('middle_name', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Sharifi')),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('employee', 'Xodim'), ('head', 'Boshliq')], max_length=20, verbose_name='Roli')),
                ('position', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Lavozimo')),
                ('gender', models.CharField(blank=True, choices=[('male', 'Erkak'), ('female', 'Ayol')], max_length=100, null=True, verbose_name='Jinsi')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name="Tug'ilgan kuni")),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/users', verbose_name='Rasmi')),
                ('country', models.CharField(blank=True, max_length=100, null=True, verbose_name='Davlati')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='Viloyati')),
                ('town', models.CharField(blank=True, max_length=100, null=True, verbose_name='Tumani')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Manzili')),
                ('phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='Telefon raqami')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faol')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Tahrirlangan vaqti')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.branch')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.department', verbose_name="Bo'limi")),
                ('working_time', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.workingtime', verbose_name='Ish vaqti')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=100)),
                ('input_status', models.CharField(blank=True, choices=[('created', 'Yaratilgan'), ('arrived', 'Kelgan'), ('late', 'Kech qolgan'), ('crash', 'Xatolik'), ('failed', 'Muvaffaqiyatsiz')], default='created', max_length=100, null=True)),
                ('output_status', models.CharField(blank=True, choices=[('created', 'Yaratilgan'), ('gone', 'Ketgan'), ('crash', 'Xatolik'), ('failed', 'Muvaffaqiyatisz')], default='created', max_length=100, null=True)),
                ('input_image', models.ImageField(blank=True, null=True, upload_to='images/controls/input')),
                ('output_image', models.ImageField(blank=True, null=True, upload_to='images/controls/output')),
                ('input_time', models.TimeField(blank=True, null=True)),
                ('output_time', models.TimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('input_area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='control_input_area', to='users.area')),
                ('output_area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='control_output_area', to='users.area')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=1000)),
                ('comment', models.CharField(max_length=1000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer_a', models.TextField()),
                ('answer_b', models.TextField()),
                ('answer_c', models.TextField()),
                ('answer_d', models.TextField()),
                ('correct_answer', models.CharField(choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], max_length=10)),
                ('score', models.IntegerField(default=2)),
                ('set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.set')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid4, max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('questions_count', models.IntegerField(default=30)),
                ('passing_score', models.IntegerField(default=50)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('duration', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('not_started', 'Boshlanmagan'), ('started', 'Boshlangan'), ('ended', 'Tugagan'), ('passed', "O'tgan"), ('failed', 'Yiqilgan')], default='created', max_length=100)),
                ('questions', models.ManyToManyField(blank=True, related_name='test_questions', to='users.question')),
                ('set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.set')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 3.2.1 on 2021-06-09 10:34

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[(1, 'GMS_ADMIN'), (2, 'Teacher'), (3, 'Student')], default=1, max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('attendance_date', models.DateField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('class_name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='GradeLevel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('gradeLevel_no', models.IntegerField(default=1)),
                ('gradelevel_name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gms_admin.classes')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SessionYearModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('session_start_year', models.DateField()),
                ('session_end_year', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='gms_admin.classes')),
                ('gradelevel_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='gms_admin.gradelevel')),
                ('session_year_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gms_admin.sessionyearmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject_name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gms_admin.classes')),
                ('gradelevel_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gms_admin.gradelevel')),
                ('teacher_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('section_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gms_admin.section')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gms_admin.students')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='gms_admin.subjects')),
                ('teacher_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='gms_admin.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Student_Grade',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('FirstQtr', models.IntegerField()),
                ('SecondQtr', models.IntegerField()),
                ('ThirdQtr', models.IntegerField()),
                ('FourthQtr', models.IntegerField()),
                ('Average', models.IntegerField()),
                ('Gwa', models.IntegerField()),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gms_admin.students')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='gms_admin.subjects')),
            ],
        ),
        migrations.CreateModel(
            name='section_subjects',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gms_admin.classes')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gms_admin.subjects')),
            ],
        ),
        migrations.CreateModel(
            name='Quizzes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='gms_admin.subjects')),
            ],
        ),
        migrations.CreateModel(
            name='Parents',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='gms_admin.subjects')),
            ],
        ),
        migrations.CreateModel(
            name='GMS_Admin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='First_Qtr',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('grade', models.IntegerField()),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gms_admin.students')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='gms_admin.subjects')),
            ],
        ),
        migrations.CreateModel(
            name='Examinations',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='gms_admin.subjects')),
            ],
        ),
        migrations.AddField(
            model_name='classes',
            name='gradelevel_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gms_admin.gradelevel'),
        ),
        migrations.AddField(
            model_name='classes',
            name='teacher_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='AttendanceReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('attendance_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gms_admin.attendance')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='gms_admin.students')),
            ],
        ),
        migrations.AddField(
            model_name='attendance',
            name='class_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gms_admin.classes'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='session_year_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gms_admin.sessionyearmodel'),
        ),
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='gms_admin.subjects')),
            ],
        ),
    ]

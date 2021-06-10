# Generated by Django 3.2.3 on 2021-06-05 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('byhand', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(blank=True, max_length=500, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('tags', models.CharField(max_length=1000, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='media')),
                ('likes', models.IntegerField(default=0)),
                ('comments', models.IntegerField(default=0)),
                ('is_deleted', models.IntegerField(default=0)),
                ('privacy', models.CharField(choices=[('1', 'Public'), ('2', 'Friends'), ('3', 'Private')], default='1', max_length=20)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('userextend', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='byhand.userextend')),
            ],
            options={
                'ordering': ['-date'],
                'get_latest_by': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Working',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=50, null=True)),
                ('availability', models.BooleanField(default=False)),
                ('start_time', models.TimeField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('breaktimef_start', models.TimeField(null=True)),
                ('breaktimef_end', models.TimeField(null=True)),
                ('breaktimes_start', models.TimeField(null=True)),
                ('breaktimes_end', models.TimeField(null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testimonial_name', models.CharField(blank=True, max_length=500, null=True)),
                ('testimonial_image', models.ImageField(blank=True, null=True, upload_to='media')),
                ('testimonial_description', models.CharField(max_length=5000, null=True)),
                ('is_approved', models.IntegerField(default=0)),
                ('is_rejected', models.IntegerField(default=0)),
                ('is_requested', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
                ('testuser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='testuser', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usert', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=50, null=True)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='social.post')),
                ('reporter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authname', models.CharField(max_length=250, null=True)),
                ('project_name', models.CharField(max_length=100, null=True)),
                ('company', models.CharField(max_length=100, null=True)),
                ('is_approved', models.IntegerField(default=0)),
                ('is_rejected', models.IntegerField(default=0)),
                ('is_requested', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
                ('auth', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auserp', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uuserp', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.IntegerField(choices=[(1, 'Like'), (2, 'Comment'), (3, 'Certifiacte'), (4, 'follow'), (5, 'endorse'), (6, 'connected')])),
                ('text_preview', models.CharField(blank=True, max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_seen', models.BooleanField(default=False)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_post', to='social.post')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='noti_from_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='noti_to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=500, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='social.post')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expertise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authname', models.CharField(max_length=250, null=True)),
                ('profession', models.CharField(max_length=500, null=True)),
                ('expertisein', models.CharField(max_length=500, null=True)),
                ('years', models.FloatField(null=True)),
                ('description', models.CharField(blank=True, max_length=5000, null=True)),
                ('is_approved', models.IntegerField(default=0)),
                ('is_rejected', models.IntegerField(default=0)),
                ('is_requested', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
                ('auth', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ausere', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eusere', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fromyear', models.DateField(null=True)),
                ('toyear', models.DateField(null=True)),
                ('company_name', models.CharField(max_length=50, null=True)),
                ('exp_keywords', models.CharField(max_length=500, null=True)),
                ('exp_detail', models.CharField(blank=True, max_length=500, null=True)),
                ('comments', models.CharField(blank=True, max_length=500, null=True)),
                ('responsibily', models.CharField(blank=True, max_length=500, null=True)),
                ('expimage', models.ImageField(blank=True, null=True, upload_to='media')),
                ('is_approved', models.IntegerField(default=0)),
                ('is_rejected', models.IntegerField(default=0)),
                ('is_requested', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DOCS', models.FileField(null=True, upload_to='media')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('bio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='byhand.bio')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='social.post')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clientname', models.CharField(max_length=500, null=True)),
                ('clientimage', models.FileField(blank=True, null=True, upload_to='media')),
                ('client_description', models.CharField(max_length=5000, null=True)),
                ('is_approved', models.IntegerField(default=0)),
                ('is_rejected', models.IntegerField(default=0)),
                ('is_requested', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userc', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cexepertise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession', models.CharField(max_length=100, null=True)),
                ('year', models.IntegerField(null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate_name', models.CharField(max_length=5000, null=True)),
                ('certificate_id', models.CharField(max_length=500, null=True)),
                ('certificate_image', models.ImageField(blank=True, null=True, upload_to='media')),
                ('certificate_description', models.CharField(max_length=5000, null=True)),
                ('company_name', models.CharField(max_length=5000, null=True)),
                ('is_approved', models.IntegerField(default=0)),
                ('is_rejected', models.IntegerField(default=0)),
                ('is_requested', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
                ('authority', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='authority', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usercer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.FileField(null=True, upload_to='media')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Brousher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brousher', models.ImageField(blank=True, null=True, upload_to='media')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.CharField(max_length=50, null=True)),
                ('branchaddress', models.CharField(max_length=5000, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Achievements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authname', models.CharField(max_length=250, null=True)),
                ('title', models.CharField(max_length=250, null=True)),
                ('description', models.CharField(blank=True, max_length=5000, null=True)),
                ('is_approved', models.IntegerField(default=0)),
                ('is_rejected', models.IntegerField(default=0)),
                ('is_requested', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
                ('auth', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ausera', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uusera', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.CharField(max_length=2000)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 2.2.9 on 2019-12-22 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_retailer', models.BooleanField(default=False)),
                ('is_customer', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'users',
                'abstract': False,
                'verbose_name': 'user',
            },
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('contactNumber', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Retailer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(blank=True, max_length=1000, null=True)),
                ('location', models.CharField(blank=True, max_length=1000, null=True)),
                ('gstin', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('pan', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('cin', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('contactNumber', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(blank=True, max_length=200, null=True)),
                ('stock', models.IntegerField(default=0)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('image', models.CharField(blank=True, max_length=1000, null=True)),
                ('merchant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Merchant')),
                ('retailer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Retailer')),
            ],
        ),
        migrations.AddField(
            model_name='merchant',
            name='retailer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Retailer'),
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.UniqueConstraint(fields=('code', 'merchant', 'retailer'), name='unique_product'),
        ),
    ]

# Generated by Django 3.2 on 2021-05-09 04:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('dni', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=20)),
                ('apellido', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('direccion', models.CharField(max_length=20)),
                ('telefono', models.IntegerField()),
                ('is_active', models.BooleanField(default=True, verbose_name='account is activated')),
                ('is_admin', models.BooleanField(default=False, verbose_name='staff account')),
                ('tipo_usuario', models.IntegerField(default=3)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('nombre', models.CharField(max_length=30)),
                ('provincia', models.CharField(max_length=25)),
                ('codigo_postal', models.IntegerField(primary_key=True, serialize=False)),
                ('pais', models.CharField(default='Argentina', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('origen', models.CharField(max_length=30)),
                ('destino', models.CharField(max_length=30)),
                ('nombre', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('km', models.IntegerField()),
                ('duracion', models.IntegerField()),
                ('duracion_en', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Tarjeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nro', models.BigIntegerField()),
                ('banco', models.CharField(max_length=20)),
                ('entidad', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('patente', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=4)),
                ('capacidad', models.IntegerField(verbose_name='Cantidad de asientos')),
                ('premium', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Viaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_salida', models.DateTimeField()),
                ('fecha_llegada', models.DateTimeField(verbose_name='%m/%d/%Y %H:%M')),
                ('hora_salida', models.CharField(max_length=20)),
                ('hora_llegada', models.CharField(max_length=20)),
                ('asientos_total', models.IntegerField(default=0)),
                ('asientos_disponibles', models.IntegerField(default=0)),
                ('vendidos', models.IntegerField()),
                ('chofer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('ciudad_destino', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='combi19app.ciudad')),
                ('ciudad_origen', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='combi19app.ciudad')),
                ('ruta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='combi19app.ruta')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='combi19app.vehiculo')),
            ],
        ),
        migrations.CreateModel(
            name='Pasajes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=20)),
                ('dni', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('nro_viaje', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='combi19app.viaje')),
                ('tarjeta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='combi19app.tarjeta')),
            ],
        ),
    ]

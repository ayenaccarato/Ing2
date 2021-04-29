# Generated by Django 3.2 on 2021-04-29 03:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('nombre', models.CharField(max_length=30)),
                ('provincia', models.CharField(max_length=25)),
                ('codigo_postal', models.IntegerField(primary_key=True, serialize=False)),
                ('pais', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ident', models.CharField(max_length=30)),
                ('nombre', models.CharField(max_length=30)),
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
            name='Usuario',
            fields=[
                ('usuario', models.CharField(max_length=15)),
                ('contraseña', models.CharField(max_length=8)),
                ('dni', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=20)),
                ('apellido', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('direccion', models.CharField(max_length=20)),
                ('telefono', models.IntegerField()),
                ('tipo_usuario', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patente', models.CharField(max_length=10)),
                ('marca', models.CharField(max_length=20)),
                ('modelo', models.CharField(max_length=20)),
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
                ('asientos_total', models.IntegerField()),
                ('asientos_disponibles', models.IntegerField()),
                ('chofer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='combi19app.usuario')),
                ('ciudad_destino', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ciudad_destino', to='combi19app.ciudad')),
                ('ciudad_origen', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ciudad_origen', to='combi19app.ciudad')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='combi19app.vehiculo')),
            ],
        ),
        migrations.CreateModel(
            name='Pasajes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=20)),
                ('dni', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='combi19app.usuario')),
                ('nro_viaje', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='combi19app.viaje')),
                ('tarjeta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='combi19app.tarjeta')),
            ],
        ),
    ]

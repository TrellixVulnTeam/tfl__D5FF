# Generated by Django 2.1.3 on 2019-02-13 06:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manifestation', models.CharField(max_length=255, null=True)),
                ('beginning', models.DateTimeField(null=True)),
                ('ending', models.DateTimeField(null=True)),
                ('delivery', models.DateTimeField(null=True)),
                ('pickup', models.DateTimeField(null=True)),
                ('email', models.EmailField(max_length=255, null=True)),
                ('personal_name', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('phone', models.CharField(max_length=255, null=True)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('total_weight', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('products', models.ManyToManyField(blank=True, to='products.CartProduct')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
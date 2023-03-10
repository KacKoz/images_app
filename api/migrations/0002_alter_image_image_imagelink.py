# Generated by Django 4.1.7 on 2023-03-08 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.CreateModel(
            name='ImageLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=16, unique=True)),
                ('is_original', models.BooleanField(default=False)),
                ('size', models.IntegerField(blank=True, null=True)),
                ('expiring', models.DateTimeField(blank=True, null=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.image')),
            ],
        ),
    ]

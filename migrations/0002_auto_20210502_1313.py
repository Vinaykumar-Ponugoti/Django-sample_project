# Generated by Django 3.2 on 2021-05-02 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Parking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkslots',
            name='colnum',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='parkslots',
            name='phnnum',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='parkslots',
            name='rownum',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='parkslots',
            name='status',
            field=models.IntegerField(),
        ),
    ]

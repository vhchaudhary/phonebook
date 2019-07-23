# Generated by Django 2.1.7 on 2019-06-24 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0002_auto_20190607_0509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='bdate',
            field=models.DateField(blank=True, null=True, verbose_name='Birth Date'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='company_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='lname',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Sur Name'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='nick_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Nick Name'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='website',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contactno',
            name='contact_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='phonebook.Contact'),
        ),
    ]
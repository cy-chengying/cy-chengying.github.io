# Generated by Django 3.0.3 on 2020-04-01 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256)),
                ('title', models.CharField(max_length=512)),
                ('content', models.TextField(max_length=256)),
                ('publish', models.DateTimeField()),
            ],
            options={
                'verbose_name': '留言板',
                'verbose_name_plural': '留言板',
            },
        ),
    ]

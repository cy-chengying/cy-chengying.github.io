# Generated by Django 3.0.3 on 2020-05-11 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='salegood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=256)),
                ('img_url', models.ImageField(upload_to='img')),
                ('name', models.CharField(max_length=200)),
                ('money', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('sort', models.CharField(choices=[('book', '书本类'), ('food', '食品类'), ('res', '物品类'), ('necessary', '日用品类'), ('other', '其他')], default='书本类', max_length=32)),
            ],
            options={
                'verbose_name': '出售货物信息',
                'verbose_name_plural': '出售货物信息',
            },
        ),
    ]

# Generated by Django 3.1.3 on 2020-11-18 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20201116_1116'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklyForecast',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.CharField(max_length=100)),
                ('week', models.IntegerField()),
                ('week_ending', models.DateField(auto_now_add=True)),
                ('topic', models.CharField(max_length=500)),
                ('references', models.TextField()),
                ('remarks', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.grade')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.subject')),
                ('teacher_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.teacher')),
                ('term_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.termmodel')),
            ],
            options={
                'db_table': 'WeeklyForecast',
            },
        ),
        migrations.DeleteModel(
            name='WeeklyLessonNotes',
        ),
    ]
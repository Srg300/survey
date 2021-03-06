# Generated by Django 2.2.10 on 2020-09-23 05:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=500)),
                ('type_question', models.CharField(choices=[('string type', 'ответ текстом'), ('pick one', 'ответ с выбором одного варианта'), ('pick many', 'ответ с выбором нескольких вариантов')], default=0, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=500)),
                ('discription', models.CharField(blank=True, default='', max_length=500)),
                ('is_active', models.BooleanField(default=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(auto_now=True)),
                ('questions', models.ManyToManyField(blank=True, to='api.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, default='', max_length=500)),
                ('surv_id', models.CharField(blank=True, default='', max_length=500)),
                ('answer', models.CharField(blank=True, default='', max_length=500)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_in_answer', to='api.Question')),
            ],
        ),
    ]

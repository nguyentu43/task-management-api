# Generated by Django 4.0.3 on 2022-03-18 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profile', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('order', models.IntegerField()),
                ('due_datetime', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Complete', 'Complete'), ('UnComplete', 'Uncomplete'), ('Draft', 'Draft')], default='UnComplete', max_length=25)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile.profile')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.section')),
                ('tags', models.ManyToManyField(blank=True, to='project.tag')),
            ],
        ),
        migrations.CreateModel(
            name='TodoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('order', models.IntegerField()),
                ('due_datetime', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_done', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='profile.profile')),
                ('participants', models.ManyToManyField(blank=True, to='profile.profile')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.task')),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Love', 'Love'), ('Like', 'Like'), ('Smile', 'Smile')], default='Like', max_length=25)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.comment')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile.profile')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.task'),
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.task')),
            ],
        ),
    ]
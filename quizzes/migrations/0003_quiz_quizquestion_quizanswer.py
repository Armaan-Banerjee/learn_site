# Generated by Django 4.0.4 on 2023-12-28 20:38

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0002_flashcard_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question', models.TextField()),
                ('quiz', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quizzes.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='QuizAnswer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('answer', models.TextField()),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quizzes.quizquestion')),
            ],
        ),
    ]

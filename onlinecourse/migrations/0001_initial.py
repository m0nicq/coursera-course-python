from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name="Instructor", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("bio", models.TextField(blank=True)),
            ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name="Learner", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name="Course", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=200, verbose_name="Название")),
            ("description", models.TextField(verbose_name="Описание")),
            ("instructors", models.ManyToManyField(blank=True, to="onlinecourse.instructor")),
        ], options={"verbose_name": "курс", "verbose_name_plural": "Курсы"}),
        migrations.CreateModel(name="Lesson", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=200, verbose_name="Название")),
            ("content", models.TextField(verbose_name="Содержание")),
            ("order", models.PositiveIntegerField(default=1)),
            ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="onlinecourse.course")),
        ], options={"ordering": ["order", "pk"], "verbose_name": "урок", "verbose_name_plural": "Уроки"}),
        migrations.CreateModel(name="Question", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("question_text", models.CharField(max_length=500, verbose_name="Вопрос")),
            ("grade", models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Баллы")),
            ("lesson", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="onlinecourse.lesson")),
        ], options={"ordering": ["lesson__order", "pk"], "verbose_name": "вопрос", "verbose_name_plural": "Вопросы"}),
        migrations.CreateModel(name="Choice", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("choice_text", models.CharField(max_length=300, verbose_name="Ответ")),
            ("is_correct", models.BooleanField(default=False, verbose_name="Правильный")),
            ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="onlinecourse.question")),
        ], options={"ordering": ["pk"], "verbose_name": "вариант ответа", "verbose_name_plural": "Варианты ответов"}),
        migrations.CreateModel(name="Submission", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("score", models.PositiveIntegerField(default=0)),
            ("total", models.PositiveIntegerField(default=0)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("learner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="onlinecourse.learner")),
            ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="onlinecourse.course")),
            ("choices", models.ManyToManyField(blank=True, to="onlinecourse.choice")),
        ], options={"verbose_name": "попытка", "verbose_name_plural": "Попытки"}),
    ]

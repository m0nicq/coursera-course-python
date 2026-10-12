from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Learner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Course(models.Model):
    name = models.CharField("Название", max_length=200)
    description = models.TextField("Описание")
    instructors = models.ManyToManyField(Instructor, blank=True)

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField("Название", max_length=200)
    content = models.TextField("Содержание")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title


class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question_text = models.CharField("Вопрос", max_length=500)
    grade = models.PositiveIntegerField("Баллы", default=1, validators=[MinValueValidator(1)])

    class Meta:
        ordering = ["lesson__order", "pk"]
        verbose_name = "вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        """Award points only when all and only the correct choices are selected."""
        correct = set(self.choice_set.filter(is_correct=True).values_list("pk", flat=True))
        return bool(correct) and correct == set(selected_ids)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField("Ответ", max_length=300)
    is_correct = models.BooleanField("Правильный", default=False)

    class Meta:
        ordering = ["pk"]
        verbose_name = "вариант ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice, blank=True)
    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "попытка"
        verbose_name_plural = "Попытки"

    def __str__(self):
        return f"{self.learner}: {self.course} ({self.score}/{self.total})"

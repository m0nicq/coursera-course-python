import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from onlinecourse.models import Choice, Course, Instructor, Learner, Lesson, Question


class Command(BaseCommand):
    help = "Create a demo admin and a course with an exam (safe to run repeatedly)."

    @transaction.atomic
    def handle(self, *args, **options):
        password = os.environ.get("DEMO_ADMIN_PASSWORD")
        if not password:
            raise CommandError("Set DEMO_ADMIN_PASSWORD before running seed_demo.")
        user, created = get_user_model().objects.get_or_create(
            username="demo", defaults={"is_staff": True, "is_superuser": True})
        if created:
            user.set_password(password)
            user.save()
        Learner.objects.get_or_create(user=user)
        instructor, _ = Instructor.objects.get_or_create(user=user)
        course, _ = Course.objects.get_or_create(
            name="Основы Django", defaults={"description": "Модели, шаблоны и обработка запросов в Django."})
        course.instructors.add(instructor)
        data = [
            ("Модели и база данных", "Модели Django описывают данные. ForeignKey задаёт связь многие-к-одному.",
             "Какое поле задаёт связь многие-к-одному?", [("ForeignKey", True), ("CharField", False)], 5),
            ("Шаблоны Django", "Тег for перебирает коллекции, а csrf_token защищает формы от CSRF.",
             "Какие теги используются в форме и для перебора уроков?",
             [("csrf_token", True), ("for", True), ("SQL SELECT", False)], 5),
            ("Обработка запросов", "POST отправляет ответы. Сервер проверяет их и рассчитывает оценку.",
             "Каким HTTP-методом отправлять ответы экзамена?", [("POST", True), ("GET", False)], 5),
        ]
        for order, (title, content, text, choices, grade) in enumerate(data, 1):
            lesson, _ = Lesson.objects.get_or_create(course=course, order=order,
                                                      defaults={"title": title, "content": content})
            question, _ = Question.objects.get_or_create(lesson=lesson, question_text=text, defaults={"grade": grade})
            for choice_text, is_correct in choices:
                Choice.objects.get_or_create(question=question, choice_text=choice_text, defaults={"is_correct": is_correct})
        self.stdout.write(self.style.SUCCESS("Demo ready. Login: demo. Course: /course/%s/" % course.pk))

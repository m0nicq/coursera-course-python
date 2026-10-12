from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Choice, Course, Learner, Lesson, Question, Submission


class ExamTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("student", password="test-password")
        self.learner = Learner.objects.create(user=self.user)
        self.course = Course.objects.create(name="Django", description="Test course")
        lesson = Lesson.objects.create(course=self.course, title="Models", content="Lesson")
        self.question = Question.objects.create(lesson=lesson, question_text="Select both", grade=15)
        self.a = Choice.objects.create(question=self.question, choice_text="A", is_correct=True)
        self.b = Choice.objects.create(question=self.question, choice_text="B", is_correct=True)
        self.c = Choice.objects.create(question=self.question, choice_text="C", is_correct=False)
        self.url = reverse("onlinecourse:submit", args=[self.course.pk])
        self.client.force_login(self.user)

    def test_pass_and_result(self):
        response = self.client.post(self.url, {"choices": [self.a.pk, self.b.pk]}, follow=True)
        self.assertContains(response, "Поздравляем")
        attempt = Submission.objects.get()
        self.assertEqual((attempt.score, attempt.total), (15, 15))
        self.assertTrue(response.context["passed"])

    def test_partial_and_extra_choices_fail(self):
        for selected in ([self.a.pk], [self.a.pk, self.b.pk, self.c.pk], []):
            response = self.client.post(self.url, {"choices": selected}, follow=True)
            self.assertFalse(response.context["passed"])
            self.assertEqual(response.context["submission"].score, 0)

    def test_invalid_choices_rejected(self):
        for selected in (["invalid"], [999999]):
            self.assertEqual(self.client.post(self.url, {"choices": selected}).status_code, 400)
        self.assertFalse(Submission.objects.exists())

    def test_other_course_choice_rejected(self):
        other = Course.objects.create(name="Other")
        lesson = Lesson.objects.create(course=other, title="Other")
        question = Question.objects.create(lesson=lesson, question_text="Other")
        choice = Choice.objects.create(question=question, choice_text="Other", is_correct=True)
        self.assertEqual(self.client.post(self.url, {"choices": [choice.pk]}).status_code, 400)

    def test_private_results(self):
        attempt = Submission.objects.create(learner=self.learner, course=self.course, score=15, total=15)
        other = get_user_model().objects.create_user("other")
        self.client.force_login(other)
        url = reverse("onlinecourse:show_exam_result", args=[self.course.pk, attempt.pk])
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_post_required_and_login_required(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)
        self.client.logout()
        self.assertEqual(self.client.post(self.url).status_code, 302)

    def test_course_displays_lessons(self):
        response = self.client.get(reverse("onlinecourse:course_details", args=[self.course.pk]))
        self.assertContains(response, "Models")
        self.assertContains(response, "Select both")

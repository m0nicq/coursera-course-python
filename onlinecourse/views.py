from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Choice, Course, Learner, Question, Submission


def index(request):
    return render(request, "onlinecourse/index.html", {"courses": Course.objects.all()})


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "onlinecourse/course_details_bootstrap.html", {
        "course": course,
        "lessons": course.lesson_set.prefetch_related("question_set__choice_set"),
    })


@login_required
@require_POST
@transaction.atomic
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = list(Question.objects.filter(lesson__course=course).prefetch_related("choice_set"))
    if not questions:
        return HttpResponseBadRequest("В курсе пока нет экзамена.")
    try:
        selected = {int(value) for value in request.POST.getlist("choices")}
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Некорректные варианты ответа.")
    allowed = set(Choice.objects.filter(question__lesson__course=course).values_list("pk", flat=True))
    if not selected <= allowed:
        return HttpResponseBadRequest("Ответы должны принадлежать этому курсу.")
    learner, _ = Learner.objects.get_or_create(user=request.user)
    score = sum(q.grade for q in questions if q.is_get_score(selected & {c.pk for c in q.choice_set.all()}))
    submission = Submission.objects.create(learner=learner, course=course,
                                           score=score, total=sum(q.grade for q in questions))
    submission.choices.set(selected)
    return redirect("onlinecourse:show_exam_result", course_id=course.pk, submission_id=submission.pk)


@login_required
def show_exam_result(request, course_id, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id, course_id=course_id,
                                   learner__user=request.user)
    selected = set(submission.choices.values_list("pk", flat=True))
    results = []
    for question in Question.objects.filter(lesson__course_id=course_id).prefetch_related("choice_set"):
        choices = list(question.choice_set.all())
        correct = question.is_get_score(selected & {c.pk for c in choices})
        results.append({"question": question, "correct": correct,
                        "choices": [{"text": c.choice_text, "selected": c.pk in selected,
                                     "correct": c.is_correct} for c in choices]})
    percent = round(submission.score / submission.total * 100, 1) if submission.total else 0
    return render(request, "onlinecourse/exam_result_bootstrap.html", {
        "submission": submission, "course": submission.course, "results": results,
        "percent": percent, "passed": submission.total > 0 and submission.score * 100 >= submission.total * 70,
    })


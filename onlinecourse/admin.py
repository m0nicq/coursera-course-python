from django.contrib import admin
from .models import Instructor, Learner, Course, Lesson, Question, Choice, Submission


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ["question_text", "lesson", "grade"]
    list_filter = ["lesson__course"]
    search_fields = ["question_text"]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ["title", "course", "order"]
    list_filter = ["course"]


admin.site.register([Instructor, Learner, Course, Choice, Submission])
admin.site.site_header = "Администрирование онлайн-курса"
admin.site.site_title = "Онлайн-курс"

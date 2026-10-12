from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = "onlinecourse"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(template_name="onlinecourse/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("course/<int:course_id>/", views.course_details, name="course_details"),
    path("course/<int:course_id>/submit/", views.submit, name="submit"),
    path("course/<int:course_id>/result/<int:submission_id>/", views.show_exam_result, name="show_exam_result"),
]

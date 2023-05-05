from django.urls import path
from .views import upload_resume, display_resume

app_name = "resume_parser"

urlpatterns = [
    path("upload/", upload_resume, name="upload"),
    path("resume-parse/<str:name>/", display_resume, name="resume_parse"),
]

# from django.shortcuts import render
# from django.http import HttpResponse
# from InterviewIQ.models import Resume
# def abcd(request):
# print(1)
# if request.method == 'POST':
# print(2)
# return render(request, "InterviewIQ/index.html", context={})

import os
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .utils import ResumeParser


def upload_resume(request):
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.FILES:
            messages.error(request, "No file part")
            return redirect(request.path_info)
        file = request.FILES["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if not file.name:
            messages.error(request, "No selected file")
            return redirect(request.path_info)
        if allowed_file(file.name):
            filename = FileSystemStorage().save(
                os.path.join(settings.MEDIA_ROOT, file.name), file
            )
            print(filename)
            resume_path = os.path.join(settings.MEDIA_ROOT, filename)
            json_data = ResumeParser().query_resume(resume_path)
            return JsonResponse(json_data)
    return render(request, "resume_parser/index.html")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "pdf",
        "doc",
        "docx",
    }


def display_resume(request, name):
    breakpoint()
    resume_path = os.path.join(settings.MEDIA_ROOT, name)
    return ResumeParser().query_resume(resume_path)

import json
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from core.models import Subject, TermModel, Student, Attendance, AttendanceReport


def teacher_home(request):
    return render(request, "teacher_template/home_content.html")


def take_attendance(request):
    subjects = Subject.objects.filter(teacher_id=request.user.id)
    terms = TermModel.object.all()
    return render(request, "teacher_template/take_attendance.html", {"subjects": subjects, "terms": terms})


@csrf_exempt
def get_students_attendance(request):
    subject_id = request.POST.get("subject")
    term = request.POST.get("term")
    subject = Subject.objects.get(id=subject_id)
    term_model = TermModel.object.get(id=term)
    students = Student.objects.filter(class_id=subject.class_id, term_id=term_model)
    list_data = []
    for student in students:
        data_small = {"id": student.admin.id, "name": student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_attendance_data(request):
    student_ids = request.POST.getlist("student_ids[]")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    term_id = request.POST.get("term_id")

    #subject_model = Subject.objects.get(id=subject_id)
    term_model = TermModel.object.get(id=term_id)
    attendance = Attendance(attendance_date=attendance_date, term_id=term_model)
    attendance.save()
    print("True")

    for stud in student_ids:
        student = Student.objects.get(id=stud)
        attendance_report = AttendanceReport(student, attendance)
        print(attendance_report)
        attendance_report.save()
        return HttpResponse("ok")

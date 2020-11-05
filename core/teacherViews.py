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
    students = Student.objects.filter(
        class_id=subject.class_id, term_id=term_model)
    list_data = []
    for student in students:
        data_small = {"id": student.admin.id,
                      "name": student.admin.first_name + " " + student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


# Attendance
@csrf_exempt
def save_attendance_data(request):
    student_ids = request.POST.get("student_ids")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    term_id = request.POST.get("term_id")

    print(student_ids)
    subject_model = Subject.objects.get(id=subject_id)
    term_model = TermModel.object.get(id=term_id)
    json_student_data = json.loads(student_ids)

    try:
        attendance = Attendance(subject_id=subject_model, attendance_date=attendance_date, term_id=term_model)
        attendance.save()

        for stud in json_student_data:
            student = Student.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def update_attendance_data(request):
    subjects = Subject.objects.filter(teacher_id=request.user.id)
    term_id = TermModel.object.all()
    attendance = Attendance.objects.all()
    return render(request,"teacher_template/update_attendance.html", {"subjects": subjects, "term_id": term_id})


@csrf_exempt
def get_attendance_dates(request):
    subject = request.POST.get("subject")
    term_id = request.POST.get("term_id")
    term_obj = TermModel.object.get(id=term_id)
    subject_obj = Subject.objects.get(id=subject)
    attendance = Attendance.objects.filter(subject_id=subject_obj, term_id=term_obj)
    attendance_obj = []
    for small_attendance in attendance:
        data = {"id": small_attendance.id, "attendance_date": str(small_attendance.attendance_date), "term_id": small_attendance.term_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj), safe=False)

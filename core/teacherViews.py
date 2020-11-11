import json
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from core.models import Subject, TermModel, Student, Attendance, AttendanceReport, Grade


def teacher_home(request):
    return render(request, "teacher_template/home_content.html")


# New attendance module I'm working on
def attendance_table(request):
    return render(request, "teacher_template/attendance_table.html")


# code starts here
def new_attendance(request):
    classes = Grade.objects.filter(teacher_id=request.user.id)
    terms = TermModel.object.all()
    return render(request, "teacher_template/att_table.html", {"classes": classes, "terms": terms})


@csrf_exempt
def get_att_table(request):
    class_id = request.POST.get("grade")
    term = request.POST.get("term")
    class_model = Grade.objects.get(id=class_id)
    term_model = TermModel.object.get(id=term)
    students = Student.objects.filter(class_id=class_model, term_id=term_model)
    list_data = []
    for student in students:
        data_small = {"id": student.admin.id, "name": student.admin.first_name + " " + student.admin.last_name, "DOB": student.date_of_birth, "admission": student.reg_number}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data, default=str), content_type="application/json", safe=False)


# Save new attendance data
@csrf_exempt
def save_new_attendance_data(request):
    student_ids = request.POST.get("student_ids")
    class_id = request.POST.get("class_id")
    attendance_date = request.POST.get("attendance_date")
    term_id = request.POST.get("term_id")

    print(student_ids)
    class_model = Grade.objects.get(id=class_id)
    term_model = TermModel.object.get(id=term_id)
    json_student_data = json.loads(student_ids)

    try:
        attendance = Attendance(class_id=class_model, attendance_date=attendance_date, term_id=term_model)
        attendance.save()

        for stud in json_student_data:
            student = Student.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def view_update_attendance(request):
    classes = Grade.objects.filter(teacher_id=request.user.id)
    term_id = TermModel.object.all()
    return render(request, "teacher_template/update_attendance.html", {"classes": classes, "term_id": term_id})


@csrf_exempt
def get_atendance_dates(request):
    grade = request.POST.get("grade")
    class_obj = Grade.objects.get(id=grade)
    term_id = request.POST.get("term_id")
    term_obj = TermModel.object.get(id=term_id)
    attendance = Attendance.objects.filter(class_id=class_obj, term_id=term_obj)
    attendance_obj = []
    for small_attendance in attendance:
        data = {"id": small_attendance.id, "attendance_date": small_attendance.attendance_date, "term_id": small_attendance.term_id.id}
        attendance_obj.append(data)
    return JsonResponse(json.dumps(attendance_obj, default=str), safe=False)


@csrf_exempt
def get_attendance_data(request):
    attendance_in = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_in)
    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []
    for att in attendance_data:
        data_small = {"id": att.student_id.admin.id, "name": att.student_id.admin.first_name + " " + att.student_id.admin.last_name, "DOB": att.student_id.date_of_birth, "admission": att.student_id.reg_number, "status": att.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data, default=str), content_type="application/json", safe=False)

@csrf_exempt
def update_attendance_data(request):
    student_ids = request.POST.get("student_ids")
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)
    json_student_data = json.loads(student_ids)

    try:
        for stud in json_student_data:
            student = Student.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport.objects.get(student_id=student, attendance_id=attendance)
            attendance_report.status = stud['status']
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

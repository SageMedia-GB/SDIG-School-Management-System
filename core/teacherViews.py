import json
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from core.models import Subject, TermModel, Student, Attendance, AttendanceReport, Grade


def teacher_home(request):
    return render(request, "teacher_template/home_content.html")


def take_attendance(request):
    classes = Grade.objects.filter(teacher_id=request.user.id)
    terms = TermModel.object.all()
    return render(request, "teacher_template/take_attendance.html", {"classes": classes, "terms": terms})


@csrf_exempt
def get_students_attendance(request):
    class_id = request.POST.get("grade")
    term = request.POST.get("term")
    grade = Grade.objects.get(id=class_id)
    term_model = TermModel.object.get(id=term)
    students = Student.objects.filter(
        class_id=grade.class_id, term_id=term_model)
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
        attendance = Attendance(
            subject_id=subject_model, attendance_date=attendance_date, term_id=term_model)
        attendance.save()

        for stud in json_student_data:
            student = Student.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(
                student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

# View and Update attendance data
def update_attendance_data(request):
    subjects = Subject.objects.filter(teacher_id=request.user.id)
    term_id = TermModel.object.all()
    attendance = Attendance.objects.all()
    return render(request, "teacher_template/update_attendance.html", {"subjects": subjects, "term_id": term_id})


@csrf_exempt
def get_attendance_dates(request):
    subject = request.POST.get("subject")
    term_id = request.POST.get("term_id")
    term_obj = TermModel.object.get(id=term_id)
    subject_obj = Subject.objects.get(id=subject)
    attendance = Attendance.objects.filter(
        subject_id=subject_obj, term_id=term_obj)
    attendance_obj = []
    for small_attendance in attendance:
        data = {"id": small_attendance.id, "attendance_date": small_attendance.attendance_date,
                "term_id": small_attendance.term_id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj), safe=False)


def attendance_table(request):
    return render(request, "teacher_template/attendance_table.html")











# New attendance module I'm working on
@csrf_exempt
def att_table(request):
    classes = Grade.objects.filter(teacher_id=request.user.id)
    terms = TermModel.object.all()
    for grade in classes:
        class_id = grade.id
        students = Student.objects.filter(class_id=class_id)
    return render(request, "teacher_template/att_table.html", {"students": students, "terms": terms, "grade": grade})


@csrf_exempt
def get_new_attendance(request):
    class_id = request.POST.get("grade")
    term = request.POST.get("term")
    grade = Grade.objects.get(id=class_id)
    term_model = TermModel.object.get(id=term)
    students = Student.objects.filter(
        class_id=grade.class_id, term_id=term_model)
    list_data = []
    for student in students:
        data_small = {"id": student.admin.id,
                      "name": student.admin.first_name + " " + student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

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
        attendance = Attendance(
            class_id=class_model, attendance_date=attendance_date, term_id=term_model)
        attendance.save()

        for stud in json_student_data:
            student = Student.objects.get(admin=stud['id'])
            print(stud['id'])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        print(stud['id'])
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

import json
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from core.forms import AddLessonNoteForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from core.models import Subject, TermModel, Student, Attendance, AttendanceReport, Grade, LessonNote, WeeklyForecast, Teacher


def teacher_home(request):
    return render(request, "teacher_template/home_content.html")


# New attendance module I'm working on
def attendance_table(request):
    return render(request, "teacher_template/attendance_table.html")


# code starts here
def new_attendance(request):
    classes = Grade.objects.filter(teacher_id=request.user.id)
    terms = TermModel.object.all()
    grade = classes
    for stud in grade:
        grade_id = stud.id
        count_students = Student.objects.filter(class_id=grade_id).count()
        male_count = Student.objects.filter(class_id=grade_id, gender="Male").count()
        female_count = Student.objects.filter(class_id=grade_id, gender="Female").count()
    return render(request, "teacher_template/att_table.html", {"classes": classes, "terms": terms, "count_students": count_students, "male_count": male_count, "female_count": female_count})


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
    attendance_status = AttendanceReport.objects.all()
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


# Lesson notes view
def lesson_notes(request):
    grades = Grade.objects.filter(teacher_id=request.user.id)
    subjects = Subject.objects.filter(teacher_id=request.user.id)
    context = {
        "grades": grades,
        "subjects": subjects
    }
    return render(request, "teacher_template/manage_lesson_notes.html", context)


def lesson_note_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        week_ending = request.POST.get("week_ending")
        class_id = request.POST.get("grade")
        class_name = Grade.objects.get(id=class_id)
        subject_id = request.POST.get("subject")
        subject = Subject.objects.get(id=subject_id)
        teacher_id = request.POST.get("teacher")
        teacher = Teacher.objects.get(id=teacher_id)
        references = request.POST.get("references")
        day = request.POST.get("day")
        topic = request.POST.get("topic")
        objectives = request.POST.get("objectives")
        teacher_learner_activities = request.POST.get("teacher_learner_activities")
        teaching_learning_materials = request.POST.get("teaching_learning_materials")
        core_points = request.POST.get("core_points")
        evaluation_and_remarks = request.POST.get("evaluation_and_remarks")
        try:
            lesson_note = LessonNote(teacher_id=teacher, class_id=class_name, subject_id=subject, week_ending=week_ending, reference=reference, day=day, topic=topic, objectives=objectives, teacher_learner_activities=teacher_learner_activities, teaching_learning_materials=teaching_learning_materials, corepoints=core_points, evaluation_and_remarks=evaluation_and_remarks)
            lesson_note.save()
            messages.success(request, "Successfully Added Lesson Note")
            return HttpResponseRedirect(reverse("lesson_notes"))
        except:
            messages.error(request, "Failed to Add Lesson Note")
            return HttpResponseRedirect(reverse("lesson_notes"))


def weekly_forecasts(request):
    subjects = Subject.objects.filter(teacher_id=request.user.id)
    grades = Grade.objects.filter(teacher_id=request.user.id)
    terms = TermModel.object.all()
    context = {
        "subjects": subjects,
        "grades": grades,
        "terms": terms
    }
    return render(request, "teacher_template/manage_weekly_forecasts.html", context)


def weekly_forecast_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        subject_id = request.POST.get("subject")
        subject = Subject.objects.get(id=subject_id)
        class_id = request.POST.get("grade")
        class_name = Grade.objects.get(id=class_id)
        term_id = request.POST.get("term")
        term = TermModel.object.get(id=term_id)
        teacher_id = request.POST.get("teacher")
        teacher = Teacher.objects.get(id=teacher_id)
        year = request.POST.get("year")
        week = request.POST.get("week")
        week_ending = request.POST.get("week_ending")
        topic = request.POST.get("topic")
        references = request.POST.get("references")
        remarks = request.POST.get("remarks")
        try:
            lesson_note = WeeklyForecast(teacher_id=teacher, subject_id=subject, class_id=class_name, term_id=term, year=year, week=week, week_ending=week_ending, topic=topic, references=references, remarks=remarks)
            lesson_note.save()
            messages.success(request, "Successfully Added Weekly Forecast")
            return HttpResponseRedirect(reverse("weekly_forecasts"))
        except:
            messages.error(request, "Failed to Add Lesson Note")
            return HttpResponseRedirect(reverse("lesson_notes"))

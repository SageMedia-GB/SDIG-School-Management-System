from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.urls import reverse

from core.forms import AddStudentForm, EditStudentForm
from core.models import CustomUser, Grade, Subject, Teacher, Student, TermModel
from django.contrib import messages


def headteacher_home(request):
    return render(request, "headteacher_template/home_content.html")


def add_teacher(request):
    return render(request, "headteacher_template/add_staff_template.html")


def add_teacher_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        address = request.POST.get("address")
        ges_reg = request.POST.get("ges_reg")
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, last_name=last_name, first_name=first_name, user_type=2)
            user.teacher.address = address
            user.teacher.ges_reg = ges_reg
            user.save()
            messages.success(request, "Successfully Added Teacher")
            return HttpResponseRedirect(reverse("add_teacher"))
        except:
            messages.error(request, "Failed to Add Teacher")
            return HttpResponseRedirect(reverse("add_teacher"))


def add_class(request):
    teachers = Teacher.objects.all()
    return render(request, "headteacher_template/add_class_template.html", {"teachers": teachers})


def add_class_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        class_name = request.POST.get("grade")
        teacher_id = request.POST.get("teacher")
        teacher = CustomUser.objects.get(id=teacher_id)
    try:
        grade_model = Grade(class_name=class_name, teacher_id=teacher)
        grade_model.save()
        messages.success(request, "Successfully Added class")
        return HttpResponseRedirect(reverse("add_class"))
    except:
        messages.error(request, "Failed to Add class")
        return HttpResponseRedirect(reverse("add_class"))


def add_student(request):
    form = AddStudentForm()
    return render(request, "headteacher_template/add_student.html", {"form": form})


def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            date_of_birth = form.cleaned_data["date_of_birth"]
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            address = form.cleaned_data["address"]
            term_id = form.cleaned_data["term_id"]
            class_id = form.cleaned_data["grade"]
            gender = form.cleaned_data["gender"]
            special_needs = form.cleaned_data["special_needs"]
            reg_number = form.cleaned_data["reg_number"]
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email, last_name=last_name, first_name=first_name, user_type=3)
                user.student.address = address
                class_obj = Grade.objects.get(id=class_id)
                user.student.class_id = class_obj
                term = TermModel.object.get(id=term_id)
                user.student.term_id = term
                user.student.date_of_birth = date_of_birth
                user.student.profile_pic = profile_pic_url
                user.student.reg_number = reg_number
                user.student.special_needs = special_needs
                user.student.gender = gender
                user.save()
                messages.success(request, "Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request, "Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form = AddStudentForm(request.POST)
            return render(request, "headteacher_template/add_student.html", {"form": form})


def add_subject(request):
    classes = Grade.objects.all()
    teachers = CustomUser.objects.filter(user_type=2)
    return render(request, "headteacher_template/add_subject.html", {"teachers": teachers, "classes": classes})


def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name = request.POST.get("subject_name")
        class_id = request.POST.get("grade")
        class_name = Grade.objects.get(id=class_id)
        teacher_id = request.POST.get("teacher")
        teacher = CustomUser.objects.get(id=teacher_id)

        try:
            subject = Subject(subject_name=subject_name, class_id=class_name, teacher_id=teacher)
            subject.save()
            messages.success(request, "Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request, "Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))


def manage_teachers(request):
    teachers = Teacher.objects.all()
    return render(request, "headteacher_template/manage_teachers.html", {"teachers": teachers})


def manage_students(request):
    students = Student.objects.all()
    return render(request, "headteacher_template/manage_students.html", {"students": students})


def manage_classes(request):
    classes = Grade.objects.all()
    return render(request, "headteacher_template/manage_classes.html", {"classes": classes})


def manage_subjects(request):
    subjects = Subject.objects.all()
    return render(request, "headteacher_template/manage_subjects.html", {"subjects": subjects})


def edit_teacher(request, teacher_id):
    teacher = Teacher.objects.get(admin=teacher_id)
    return render(request, "headteacher_template/edit_teacher.html", {"teacher": teacher, "id": teacher_id})


def edit_teacher_save(request):
    if request.method != "POST":
        return HttpResponse("<h4>Method Not Allowed</h4>")
    else:
        teacher_id = request.POST.get("teacher_id")
        ges_reg = request.POST.get("ges_reg")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.get(id=teacher_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            teacher_model = Teacher.objects.get(admin=teacher_id)
            teacher_model.ges_reg = ges_reg
            teacher_model.address = address
            teacher_model.save()
            messages.success(request, "Successfully edited teacher")
            return HttpResponseRedirect(reverse("edit_teacher", kwargs={"teacher_id": teacher_id}))
        except:
            messages.error(request, "Failed to edit teacher")
            return HttpResponseRedirect(reverse("edit_teacher",kwargs={"teacher_id": teacher_id}))


def edit_student(request, student_id):
    request.session['student_id'] = student_id
    student = Student.objects.get(admin=student_id)
    form = EditStudentForm()
    form.fields['reg_number'].initial = student.reg_number
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['date_of_birth'].initial = student.date_of_birth
    form.fields['gender'].initial = student.gender
    form.fields['grade'].initial = student.class_id.id
    form.fields['username'].initial = student.admin.username
    form.fields['email'].initial = student.admin.email
    form.fields['address'].initial = student.address
    form.fields['term_id'].initial = student.term_id.id
    form.fields['profile_pic'].initial = student.profile_pic
    form.fields['special_needs'].initial = student.special_needs
    return render(request, "headteacher_template/edit_student.html", {"form": form, "id": student_id, "username": student.admin.username})


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id = request.session.get("student_id")
        if student_id is None:
            return HttpResponseRedirect(reverse("manage_student"))

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            reg_number = form.cleaned_data["reg_number"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            date_of_birth = form.cleaned_data['date_of_birth']
            class_id = form.cleaned_data["grade"]
            gender = form.cleaned_data["gender"]
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            address = form.cleaned_data["address"]
            term_id = form.cleaned_data["term_id"]
            special_needs = form.cleaned_data["special_needs"]

            if request.FILES.get('profile_pic', False):
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                student = Student.objects.get(admin=student_id)
                student.reg_number = reg_number
                student.date_of_birth = date_of_birth
                student.address = address
                class_name = Grade.objects.get(id=class_id)
                student.class_id = class_name
                student.gender = gender
                term = TermModel.object.get(id=term_id)
                student.term_id = term
                if profile_pic_url is not None:
                    student.profile_pic = profile_pic_url
                student.special_needs = special_needs
                student.save()
                del request.session['student_id']
                messages.success(request, "Successfully edited student")
                return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))
            except:
                messages.error(request, "Failed to edit student")
                return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))
        else:
            form = EditStudentForm(request.POST)
            student = Student.objects.get(admin=student_id)
            return render(request, "headteacher_template/edit_student.html", {"form": form, "id": student_id, "username": student.admin.username})


def edit_subject(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    classes = Grade.objects.all()
    teachers = CustomUser.objects.filter(user_type=2)
    return render(request, "headteacher_template/edit_subject.html", {"subject": subject, "classes": classes, "teachers": teachers, "id": subject_id})


def edit_subject_save(request):
    if request.method != "POST":
        HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        teacher_id = request.POST.get("teacher")
        class_id = request.POST.get("grade")
        try:
            subject = Subject.objects.get(id=subject_id)
            subject.subject_name = subject_name
            teacher = CustomUser.objects.get(id=teacher_id)
            subject.teacher_id = teacher
            grade = Grade.objects.get(id=class_id)
            subject.class_id = grade
            subject.save()
            messages.success(request, "Successfully edited subject")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id": subject_id}))
        except:
            messages.error(request, "Failed to edit class")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id": subject_id}))


def edit_class(request, class_id):
    grade = Grade.objects.get(id=class_id)
    return render(request, "headteacher_template/edit_class.html", {"grade": grade, "id": class_id})


def edit_class_save(request):
    if request.method != "POST":
        HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        class_id = request.POST.get("class_id")
        class_name = request.POST.get("grade")

        try:
            grade = Grade.objects.get(id=class_id)
            grade.class_name = class_name
            grade.save()
            messages.success(request, "Successfully edited class")
            return HttpResponseRedirect(reverse("edit_class", kwargs={"class_id": class_id}))
        except:
            messages.error(request, "Failed to edit class")
            return HttpResponseRedirect(reverse("edit_class", kwargs={"class_id": class_id}))


def manage_terms(request):
    return render(request, "headteacher_template/manage_terms.html")

def add_term_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manage_terms"))
    else:
        term_start = request.POST.get("term_start")
        term_end = request.POST.get("term_end")
        try:
            term = TermModel(term_start=term_start, term_end=term_end)
            term.save()
            messages.success(request, "Successfully added term")
            return HttpResponseRedirect(reverse("manage_terms"))
        except:
            messages.error(request, "Failed to add term")
            return HttpResponseRedirect(reverse("manage_terms"))


def attendance_tables(request):
    return render(request, "headteacher_template/attendance_tables.html")

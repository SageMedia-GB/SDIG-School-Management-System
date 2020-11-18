from django import forms
from core.models import Grade, TermModel, Subject



class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    reg_number = forms.CharField(label="Reg Number", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    date_of_birth = forms.DateField(label="Date Of Birth", widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    gender = forms.ChoiceField(label="Gender", choices=gender_choice, widget=forms.Select(attrs={"class": "form-control"}))
    grade_list = []
    grades = Grade.objects.all()
    for grade in grades:
        small_grade = (grade.id, grade.class_name)
        grade_list.append(small_grade)

    term_list = []
    terms = TermModel.object.all()
    for term in terms:
        small_term = (term.id, str(term.term_start) + "  -  " + str(term.term_end))
        term_list.append(small_term)

    grade = forms.ChoiceField(label="Class", choices=grade_list, widget=forms.Select(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    term_id = forms.ChoiceField(label="Term", widget=forms.Select(attrs={"class": "form-control"}), choices=term_list)
    profile_pic = forms.FileField(label="Profile Pic", widget=forms.FileInput(attrs={"class": "form-control"}), required=False)
    special_needs = forms.CharField(label="Special Needs", max_length=50, widget=forms.Textarea(attrs={"class": "form-control"}))


class EditStudentForm(forms.Form):
    reg_number = forms.CharField(label="Reg Number", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last_name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    date_of_birth = forms.DateField(label="Date Of Birth", widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    gender = forms.ChoiceField(label="Gender", choices=gender_choice, widget=forms.Select(attrs={"class": "form-control"}))
    grade_list = []

    try:
        grades = Grade.objects.all()
        for grade in grades:
            small_grade = (grade.id, grade.class_name)
            grade_list.append(small_grade)
    except:
        grade_list = []

    term_list = []

    try:
        terms = TermModel.object.all()
        for term in terms:
            small_term = (term.id, str(term.term_start)+" - "+str(term.term_end))
            term_list.append(small_term)
    except:
        term_list = []

    grade = forms.ChoiceField(label="Grade", choices=grade_list, widget=forms.Select(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    term_id = forms.ChoiceField(label="Term", widget=forms.Select(attrs={"class": "form-control"}),choices=term_list)
    profile_pic = forms.FileField(label="Profile Pic", widget=forms.FileInput(attrs={"class": "form-control"}), required=False)
    special_needs = forms.CharField(label="Special Needs", max_length=50, widget=forms.Textarea(attrs={"class": "form-control"}))


class AddLessonNoteForm(forms.Form):
    week_ending = forms.DateField(label="Week Ending", widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    reference = forms.CharField(label="Reference", max_length=500, widget=forms.TextInput(attrs={"class": "form-control"}))
    day = forms.DateField(label="Day", widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    topic = forms.CharField(label="Topic", max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    Objectives = forms.CharField(label="Objectives", widget=forms.Textarea(attrs={"class": "form-control"}))
    teacher_learner_activities = forms.CharField(label="Teacher Learner Activities", widget=forms.Textarea(attrs={"class": "form-control", "type": "date"}))
    teaching_learning_materials = forms.ChoiceField(label="Teaching Learning Materials", widget=forms.Textarea(attrs={"class": "form-control"}))
    core_points = forms.CharField(label="Core Points", widget=forms.Textarea(attrs={"class": "form-control"}))
    evaluation_and_remarks = forms.CharField(label="Evaluation And Remarks", max_length=50, widget=forms.Textarea(attrs={"class": "form-control"}))


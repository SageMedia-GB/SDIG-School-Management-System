from django import forms

from core.models import Grade, TermModel


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    reg_number = forms.CharField(label="Reg Number", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last_name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
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

    grade = forms.ChoiceField(label="Grade", choices=grade_list, widget=forms.Select(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    term_id = forms.ChoiceField(label="Term", widget=forms.Select(attrs={"class": "form-control"}),choices=term_list)
    profile_pic = forms.FileField(label="Profile Pic", widget=forms.FileInput(attrs={"class": "form-control"}), required=False)
    special_needs = forms.CharField(label="Special Needs", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))


class EditStudentForm(forms.Form):
    reg_number = forms.CharField(label="Reg Number", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last_name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
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
    special_needs = forms.CharField(label="Special Needs", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
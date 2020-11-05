from django.urls import path

from . import headViews, teacherViews, studentViews
from .views import index_page, login_page, login_action, GetUserDetails, logout_user


urlpatterns = [
    path('', login_page, name="show_login"),
    path('index', index_page),
    path('login', login_action, name="login"),
    path('get_user_details', GetUserDetails),
    path('logout_user', logout_user, name="logout"),
    path('headteacher_home', headViews.headteacher_home, name="headteacher_home"),
    path('add_teacher', headViews.add_teacher, name="add_teacher"),
    path('add_teacher_save', headViews.add_teacher_save, name="add_teacher_save"),
    path('add_class', headViews.add_class, name="add_class"),
    path('add_class_save', headViews.add_class_save, name="add_class_save"),
    path('add_student', headViews.add_student, name="add_student"),
    path('add_student_save', headViews.add_student_save, name="add_student_save"),
    path('add_subject', headViews.add_subject, name="add_subject"),
    path('add_subject_save', headViews.add_subject_save, name="add_subject_save"),
    path('manage_teachers', headViews.manage_teachers, name="manage_teachers"),
    path('manage_students', headViews.manage_students, name="manage_students"),
    path('manage_classes', headViews.manage_classes, name="manage_classes"),
    path('manage_subjects', headViews.manage_subjects, name="manage_subjects"),
    path('edit_teacher/<str:teacher_id>', headViews.edit_teacher, name="edit_teacher"),
    path('edit_teacher_save', headViews.edit_teacher_save, name="edit_teacher_save"),
    path('edit_student/<str:student_id>', headViews.edit_student, name="edit_student"),
    path('edit_student_save', headViews.edit_student_save, name="edit_student_save"),
    path('edit_subject/<str:subject_id>', headViews.edit_subject, name="edit_subject"),
    path('edit_subject_save', headViews.edit_subject_save, name="edit_subject_save"),
    path('edit_class/<str:class_id>', headViews.edit_class, name="edit_class"),
    path('edit_class_save', headViews.edit_class_save, name="edit_class_save"),
    path('manage_terms', headViews.manage_terms, name="manage_terms"),
    path('add_term_save', headViews.add_term_save, name="add_term_save"),
    # Urls for teachers
    path('teacher_home', teacherViews.teacher_home, name="teacher_home"),
    path('take_attendance', teacherViews.take_attendance, name="take_attendance"),
    path('get_students_attendance', teacherViews.get_students_attendance, name="get_students_attendance"),
    path('save_attendance_data', teacherViews.save_attendance_data, name="save_attendance_data"),
    path('get_attendance_dates', teacherViews.get_attendance_dates, name="get_attendance_dates"),
    path('update_attendance_data', teacherViews.update_attendance_data, name="update_attendance_data"),
    # Urls for students
    path('student_home', studentViews.student_home, name="student_home")
]

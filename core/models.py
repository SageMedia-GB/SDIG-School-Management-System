from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField


class CustomUser(AbstractUser):
    user_type_data = ((1, "Headteacher"), (2, "Teacher"), (3, "Student"), (4, "CircuitSupervisor"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class School(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    headteacher = models.CharField(max_length=200)
    assistant_headteacher = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    population = models.IntegerField()
    local_authority = models.CharField(max_length=200)
    contact = models.IntegerField()
    email = models.EmailField()
    objects = models.Manager()

    class Meta:
        db_table = 'School'

    def __str__(self):
        return self.name


class TermModel(models.Model):
    id = models.AutoField(primary_key=True)
    term_start = models.DateField()
    term_end = models.DateField()
    object = models.Manager()


class Headteacher(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ges_reg = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'Headteachers'

    def __str__(self):
        return self.admin


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ges_reg = models.CharField(max_length=200)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'Teachers'

"""     def __str__(self):
        return self.admin """


class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=200)
    teacher_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'Grades'

    def __str__(self):
        return self.class_name


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=200)
    class_id = models.ForeignKey(Grade, on_delete=models.CASCADE, default=1)
    teacher_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'Subjects'

    def __str__(self):
        return self.subject_name


class Guardian(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.IntegerField()
    email = models.EmailField()
    is_parent = models.BooleanField(default=True)
    objects = models.Manager()

    class Meta:
        db_table = 'Guardians'

    def __str__(self):
        return self.first_name


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    reg_number = models.CharField(max_length=200)
    date_of_birth = models.DateField(auto_now_add=True)
    password = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    profile_pic = models.FileField()
    address = models.TextField()
    special_needs = models.TextField()
    class_id = models.ForeignKey(Grade, on_delete=models.DO_NOTHING)
    term_id = models.ForeignKey(TermModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'Students'

    def __str__(self):
        return self.admin


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(Grade, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField(auto_now_add=True)
    term_id = models.ForeignKey(TermModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'Attendance'


class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'AttendanceReports'


class StudentLeave(models.Model):
    id = models.AutoField(primary_key=True)
    Student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=200)
    leave_message = models.TextField()
    leave_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'StudentLeave'


class TeacherLeave(models.Model):
    id = models.AutoField(primary_key=True)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=200)
    leave_message = models.TextField()
    leave_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'TeacherLeave'


class StudentFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=200)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'StudentFeedback'


class TeacherFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=200)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'TeacherFeedback'


class StudentNotification(models.Model):
    id = models.AutoField(primary_key=True)
    Student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'StudentNotifications'


class TeacherNotification(models.Model):
    id = models.AutoField(primary_key=True)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'TeacherNotifications'


class CircuitSupervisor(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    local_authority = models.CharField(max_length=200)
    contact = models.IntegerField()
    school = models.CharField(max_length=200)
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'CircuitSupervisors'

    def __str__(self):
        return self.admin


class LessonNote(models.Model):
    id = models.AutoField(primary_key=True)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Grade, on_delete=models.CASCADE)
    week_ending = models.DateField()
    reference = models.CharField(max_length=500)
    day = models.CharField(max_length=500)
    topic = models.CharField(max_length=500)
    objectives = models.CharField(max_length=500)
    teacher_learner_activities = models.CharField(max_length=500)
    teaching_learning_materials = models.CharField(max_length=500)
    corepoints = models.CharField(max_length=500)
    evaluation_and_remarks = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'LessonNotes'

    def __str__(self):
        return self.topic


class WeeklyForecast(models.Model):
    id = models.AutoField(primary_key=True)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Grade, on_delete=models.CASCADE)
    term_id = models.ForeignKey(TermModel, on_delete=models.CASCADE)
    year = models.CharField(max_length=100)
    week = models.IntegerField()
    week_ending = models.DateField(auto_now_add=True)
    topic = models.CharField(max_length=500)
    references = models.TextField()
    remarks = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'WeeklyForecast'

    def __str__(self):
        return self.topic


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Headteacher.objects.create(admin=instance)
        if instance.user_type == 2:
            Teacher.objects.create(admin=instance)
        if instance.user_type == 3:
            Student.objects.create(admin=instance, class_id=Grade.objects.get(id=1), term_id=TermModel.object.get(id=1), profile_pic="", gender="Male", reg_number="ad", special_needs="special")
        if instance.user_type == 4:
            CircuitSupervisor.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.headteacher.save()
    if instance.user_type == 2:
        instance.teacher.save()
    if instance.user_type == 3:
        instance.student.save()
    if instance.user_type == 4:
        instance.circuitsupervisor.save()

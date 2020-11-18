from ckeditor.fields import RichTextField
# add 'ckeditor' to installed apps o settings.py
# add '{form.media}' to form template

class DailyLessonNotes():
    id = PrimaryKey
    teacher_id= User
    subject_id = subject
    class_id = grade
    day = DateField
    topic = textfield
    objectives = TextField
    teacher_learner_activities = RichTextField(blank=True, null=True)
    teaching_learning_materials = Textfield
    corepoints = RichTextField
    evaluation_and_remarks = textfield

    


class WeeklyLessonNotes():
    id = PrimaryKey
    user = user
    done = BooleanField
    daily_note = Many_to_ManyField
    Start_date = DateField
    end_date = DateField


class LessonArchive():
    id = PrimaryKey
    daily_notes = ForeinKey => Daily_Notes
    weekly_notes = ForeinKey => Weekly_Notes

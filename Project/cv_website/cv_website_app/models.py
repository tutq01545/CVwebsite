from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

MAX_CHAR_FIELD_LENGTH = 255
MIN_CHAR_FIELD_LENGTH = 36


# Create your models here.
class AboutMe(models.Model):
    summary = models.CharField(blank=False, max_length=MAX_CHAR_FIELD_LENGTH)

    def __str__(self):
        return "{}".format(self.summary)


class WorkExperience(models.Model):
    job_title = models.CharField(blank=False, max_length=MAX_CHAR_FIELD_LENGTH)
    employer = models.CharField(blank=False, max_length=MAX_CHAR_FIELD_LENGTH)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    description = models.CharField(blank=True, max_length=MAX_CHAR_FIELD_LENGTH)
    owner = models.ForeignKey(AboutMe, on_delete=models.CASCADE)

    def __str__(self):
        return "{} at {}".format(self.job_title, self.employer)


class Education(models.Model):
    university = models.CharField(blank=False, max_length=MAX_CHAR_FIELD_LENGTH)
    field_of_study = models.CharField(blank=False, max_length=MIN_CHAR_FIELD_LENGTH)
    degree = models.CharField(blank=False, max_length=MIN_CHAR_FIELD_LENGTH)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    description = models.CharField(blank=True, max_length=MAX_CHAR_FIELD_LENGTH)
    owner = models.ForeignKey(AboutMe, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {} in {}".format(self.degree, self.field_of_study, self.university)


class Skill(models.Model):
    skill = models.CharField(blank=False, max_length=MIN_CHAR_FIELD_LENGTH)
    leverage = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    owner = models.ForeignKey(AboutMe, on_delete=models.CASCADE)


class Hobby(models.Model):
    description = models.CharField(blank=False, max_length=MAX_CHAR_FIELD_LENGTH)
    owner = models.ForeignKey(AboutMe, on_delete=models.CASCADE)


class Link(models.Model):
    label = models.CharField(blank=False, max_length=MIN_CHAR_FIELD_LENGTH)
    link = models.CharField(blank=False, max_length=MAX_CHAR_FIELD_LENGTH)
    owner = models.ForeignKey(AboutMe, on_delete=models.CASCADE)


class Question(models.Model):
    questioner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(blank=False, max_length=MIN_CHAR_FIELD_LENGTH)
    content = models.CharField(blank=False, max_length=MAX_CHAR_FIELD_LENGTH)
    question_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} by {}".format(self.question, self.questioner.username)


class Answer(models.Model):
    answer = models.CharField(blank=False, max_length=MIN_CHAR_FIELD_LENGTH)
    related_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{}".format(self.answer)

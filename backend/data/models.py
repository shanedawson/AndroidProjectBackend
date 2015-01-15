from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Student(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=128)
    user = models.OneToOneField(
        'auth.User', related_name='student', editable=False, null=True, unique=True
    )

    def _str_(self):
        return "%s %s" % (self.last_name, self.first_name)

    def full_name(self):
        return "%s %s" % (self.last_name, self.first_name)

    def as_dict(self):
        return {"id": self.user.username}


class TAttendance(models.Model):
    owner = models.ForeignKey(Student, null=True)
    week = models.IntegerField()
    day = models.IntegerField()
    am = models.BooleanField(default=False)
    pm = models.BooleanField(default=False)

    def _str_(self):
        return self._id


class CAttendance(models.Model):
    owner = models.ForeignKey(Student, null=True)
    week = models.IntegerField()
    signature = models.TextField()
    comments = models.TextField()

    def _str_(self):
        return self._id


class SelfAssesment(models.Model):
    owner = models.ForeignKey(Student, null=True)
    task = models.IntegerField()
    diag = models.CharField(max_length=256)
    well = models.TextField()
    improve = models.TextField()
    mark = models.IntegerField()

    def _str_(self):
        return self._id + 'self_assesment'


class SelfAssesmentCont(models.Model):
    owner = models.ForeignKey(Student, null=True)
    question_one = models.TextField()
    question_two = models.TextField()
    question_one_mark = models.IntegerField()
    question_two_mark = models.IntegerField()
    mark = models.IntegerField()


class AttendanceKey(models.Model):
    value = models.CharField(max_length=6)


class FormativeCase(models.Model):
    owner = models.ForeignKey(Student, null=True)
    case = models.IntegerField()
    question_one_mark = models.IntegerField()
    question_two_mark = models.IntegerField()
    question_three_mark = models.IntegerField()
    comment = models.TextField()


class SummativeCase(models.Model):
    owner = models.ForeignKey(Student, null=True)
    question_one_a = models.FloatField()
    question_one_b = models.FloatField()
    question_one_mark = models.FloatField()
    question_two_a = models.FloatField()
    question_two_b = models.FloatField()
    question_two_mark = models.FloatField()
    question_three_a = models.FloatField()
    question_three_b = models.FloatField()
    question_three_mark = models.FloatField()
    total = models.FloatField()

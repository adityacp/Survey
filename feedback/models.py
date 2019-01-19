from django.db import models
from django.utils import timezone


question_types = [("Subjective", "Subjective"), ("Choices", "Choices"),
                  ("Rating", "Rating")]

OPD = [("Private", "Private"), ("Hospital", "Hospital")]

section = [(1, "Tinnitus prevalence"), (2, "Tinnitus matching device"),
           (3, "e-solution")]


class Profile(models.Model):
    name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    phone_no = models.CharField(max_length=10)
    experience = models.IntegerField()
    avg_opd_per_day = models.IntegerField()
    avg_surgery_per_day = models.IntegerField()
    opd = models.CharField(max_length=255, choices=OPD)
    chemist_feedback = models.TextField(null=True, blank=True)

    def __str__(self):
        return "Profile of {0}".format(self.name.title())


class Question(models.Model):
    description = models.TextField()
    type = models.CharField(max_length=255, choices=question_types)
    section = models.IntegerField(choices=section)

    def get_section(self):
        return section[self.section-1][1]

    def __str__(self):
        return "Question from {0} of type {1}".format(
            self.get_section(), self.type
        )


class Answer(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    attempt_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Answer of {0} for Question {1}".format(
            self.user.name.title(), self.question.id
        )


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return "Option for question {0}".format(self.question.id)

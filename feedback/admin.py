from django.contrib import admin

# Register your models here.
from feedback.models import Question, Option, Profile, Answer

admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Profile)
admin.site.register(Answer)

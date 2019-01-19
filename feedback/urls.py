from django.urls import path

# Local Imports
from feedback import views

app_name = "feedback"

urlpatterns = [
    path("", views.index, name="index"),
    path('add/question', views.add_or_edit_question, name="add_question"),
    path('edit/question/<int:question_id>', views.add_or_edit_question,
         name="edit_question"),
    path('add/doctor/profile', views.add_or_edit_doctor_profile,
         name="add_doctor_profile"),
    path('edit/doctor/profile/<int:profile_id>',
         views.add_or_edit_doctor_profile, name="edit_doctor_profile"),
    path('start/feedback/<int:profile_id>', views.start_feedback,
         name="start_feedback"),
    path('doctors', views.get_doctors, name="doctors"),
    path('next/section/<int:section_id>/<int:profile_id>',
         views.next_section, name="next_section"),
    path('questions', views.all_questions, name="all_questions"),
    path('view/feedback/<int:profile_id>', views.view_feedback,
         name="view_feedback"),
]

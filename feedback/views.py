from django.shortcuts import render
from django.forms import inlineformset_factory


# Local imports
from feedback.models import Question, Option, Profile, section, Answer
from feedback.forms import QuestionForm, ProfileForm


def _get_section_name(section_id):
    return section[section_id-1][1]


def index(request):
    return render(request, 'index.html')


def get_doctors(request):
    profiles = Profile.objects.all()
    return render(request, 'doctors.html', {'profiles': profiles})


def add_or_edit_doctor_profile(request, profile_id=None):
    profile = None
    if profile_id is not None:
        profile = Profile.objects.get(id=profile_id)
    profile_form = ProfileForm(instance=profile)

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile = profile_form.save()
            profile_id = profile.id

    return render(request, 'add_profile.html',
                  {'profile_form': profile_form, "profile_id": profile_id}
                  )


def start_feedback(request, profile_id=None):
    questions = Question.objects.all()
    answers_count = Answer.objects.filter(user_id=profile_id).count()
    if answers_count >= questions.count():
        msg = "You have already submitted the feedback"
        return render(request, 'feedback_done.html', {"message": msg})
    questions = questions.filter(section=1).order_by("id")
    return render(request, 'feedback.html',
                  {"questions": questions, "profile_id": profile_id,
                   "section_id": 1,
                   "section": "Tinnitus prevalence"}
                  )


def next_section(request, section_id, profile_id):
    """
        GET next section after submitting previous section
    """
    user = Profile.objects.get(id=profile_id)
    question_list = request.POST.getlist("question_id")
    current_ques = Question.objects.filter(id__in=question_list).order_by("id")
    for question in current_ques:
        if question.type == "Subjective":
            answer = request.POST.get("subjective_{0}".format(question.id))
        elif question.type == "Rating":
            answer = request.POST.get("rate_{0}".format(question.id))
        else:
            answer = request.POST.get("option_{0}".format(question.id))
        Answer.objects.get_or_create(
            user=user, answer=answer, question=question
        )
    section_id = section_id + 1
    if section_id > 3:
        msg = "Thank you for submitting the feedback"
        return render(request, 'feedback_done.html', {"message": msg})
    new_questions = Question.objects.filter(section=section_id).order_by("id")
    section_name = _get_section_name(section_id)
    return render(request, 'feedback.html',
                  {"questions": new_questions, "profile_id": profile_id,
                   "section_id": section_id,
                   "section": section_name}
                  )


def add_or_edit_question(request, question_id=None):
    """ Add feedback questions """

    question = None

    if question_id is not None:
        question = Question.objects.get(id=question_id)
    QuestionFormSet = inlineformset_factory(Question, Option,
                                            fields='__all__', extra=0)
    question_form = QuestionForm(instance=question)

    if request.method == 'POST':
        formset = QuestionFormSet(request.POST, instance=question)
        question_form = QuestionForm(request.POST, instance=question)
        if question_form.is_valid():
            question = question_form.save()
            question_id = question.id
        if formset.is_valid():
            formset.save()
        if 'add' in request.POST:
            QuestionFormSet = inlineformset_factory(
                Question, Option, fields='__all__', extra=1
                )
    formset = QuestionFormSet(instance=question)

    return render(request, 'add_question.html',
                  {'formset': formset, 'question': question,
                   'question_form': question_form, "question_id": question_id,
                   }
                  )


def all_questions(request):
    questions = Question.objects.all()
    return render(request, 'questions.html', {'questions': questions})


def view_feedback(request, profile_id):
    answers = Answer.objects.filter(user_id=profile_id)
    return render(request, 'view_feedback.html', {'answers': answers})

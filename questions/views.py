from django.views.generic import TemplateView, CreateView, FormView, ListView, DetailView
from questions.forms import RegistrationForm, LoginForm, QuestionForm, AnswerForm
from django.urls import reverse_lazy
from questions import models
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.cache import never_cache




def signin_required(fn):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            return fn(request, *args, **kwargs)
    return wrapper

decs = [signin_required, never_cache]
'''for simply viewing a template we can use this'''
# class IndexView(TemplateView):
#     template_name = 'home.html'

@method_decorator(decs, name='dispatch')
class IndexView(CreateView, ListView):
    template_name = 'home.html'
    model = models.Questions
    form_class=QuestionForm
    success_url = reverse_lazy('index')
    context_object_name = 'questions'
    def get_queryset(self):
        return models.Questions.objects.all().exclude(user=self.request.user)

    '''this is required because we are not providing the user to the Questions model where the user is required'''
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    '''another way of adding the user'''
    # def post(self, request, *args, **kwargs):
    #     form =QuestionForm(request.POST)
    #     if form.is_valid():
    #         qs = form.save(commit=False)
    #         qs.user = request.user
    #         qs.save
    #         return redirect('index')
    def get_queryset(self):
        return self.model.objects.all().exclude(user=self.request.user)
        
        
@never_cache
@signin_required
def signoutview(request, *args, **kwargs):
    logout(request)
    return redirect('login')

    
class SignupView(CreateView):
    template_name='registration.html'
    form_class=RegistrationForm
    model= models.MyUser
    success_url = reverse_lazy('registration')


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('user_name')
            pwd = form.cleaned_data.get('password')
            usr = authenticate(request, username=uname, password=pwd)
            if usr:
                login(request, usr)
                messages.success(request, 'successfully logged in')
                return redirect('index')
            else:
                messages.error(request, 'authentication failed')
                return render(request, self.template_name, {'form':form})


@method_decorator(decs, name='dispatch')
class QuestionDetailView(DetailView, FormView):
    model=models.Questions
    pk_url_kwarg='id'
    template_name='question-detail.html'
    context_object_name = 'questions'
    form_class=AnswerForm

@never_cache
@signin_required
def post_answer(request, *args, **kwargs):
    if request.method == 'POST':
        ans = AnswerForm(request.POST)
        if ans.is_valid():
            answer_in_form = ans.cleaned_data.get('answer')
            qs_id = kwargs.get('id')
            qs = models.Questions.objects.get(id=qs_id)
            models.Answers.objects.create(question=qs, user=request.user, answer=answer_in_form)
            return redirect('index')
        else:
            return redirect('index')
    '''other way'''
    # ans = request.POST.get('answer')
    # if len(ans)<1:
    #     return redirect('index')
    # else:
    #     qid = kwargs.get('id')
    #     qs = models.Questions.objects.get(id=qid)
    #     # qs.answer_set.create(user=request.user, answer=ans)
    #     models.Answers.objects.create(question=qs, user=request.user, answer=ans)
    #     return redirect('index')

@never_cache
@signin_required
#localhost:8000/questions/answers/{id}/upvote
def upvote_answer(request, *args, **kwargs):
    ans_id = kwargs.get('id')
    ans = models.Answers.objects.get(id=ans_id)
    ans.upvotes.add(request.user)
    ans.save()     
    return redirect('index')

@never_cache
@signin_required
#localhost:8000/question-detail/answers/id/delete
def delete_answer(request, *args, **kwargs):
    ans_id = kwargs.get('id')
    qs = models.Answers.objects.get(id=ans_id)
    qs.delete()
    return redirect('index')
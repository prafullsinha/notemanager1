from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from .forms import NoteModelForm, RegisterForm, CommentModelForm
from .models import NoteModel, CommentModel, LikeModel
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
import datetime


# Create your views here.
class Signup(TemplateView):
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create(username=form.cleaned_data['email'],
                                       password=make_password(form.cleaned_data['password1']),
                                       first_name=form.cleaned_data['first_name'])
            login(request, user)
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class HomeView(TemplateView):
    template_name = 'note/home.html'

    def get(self, request, *args, **kwargs):
        q = NoteModel.objects.all()
        context = {
            'q': q
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class PostView(TemplateView):
    template_name = 'note/post.html'

    def get(self, request, *args, **kwargs):
        form = NoteModelForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        profile = NoteModel()
        form = NoteModelForm(request.POST)
        if form.is_valid():
            profile1 = form.save(commit=False)
            profile1.user = request.user
            profile1.date = datetime.date.today()
            profile1.save()
            return redirect('home')
        else:
            form = NoteModelForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


@login_required()
def EditView(request, title):
    post = NoteModel.objects.get(title=title)
    if request.method == "POST":
        form = NoteModelForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('detail', title=post.title)
    else:
        form = NoteModelForm(instance=post)
    template = 'note/edit.html'
    context = {
        'form': form,
        'post': post
    }
    return render(request, template, context)


class SearchView(ListView):
    model = NoteModel
    template_name = 'note/search.html'

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        form = NoteModel.objects.get(title=query)
        context = {
            'e': form
        }
        return render(request, self.template_name, context)


class FilterView(ListView):
    model = NoteModel
    template_name = 'note/filter.html'

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        form = NoteModel.objects.filter(date=query)
        context = {
            'form': form,
            'query': query
        }
        return render(request, self.template_name, context)


class Filter1View(ListView):
    model = NoteModel
    template_name = 'note/filter1.html'

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        form = NoteModel.objects.filter(categories=query)
        context = {
            'form': form,
            'query': query
        }
        return render(request, self.template_name, context)


@login_required()
def DetailView(request, title, *args, **kwargs):
    post = NoteModel.objects.get(title=title)
    norm = CommentModel.objects.filter(note=post)
    form = CommentModelForm(request.POST or None)
    form2 = LikeModel.objects.filter(note=post)
    count = 0
    for e in form2:
        count = count + 1
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formOne':
            com = LikeModel()
            for e in form2:
                if e.user == request.user and e.note == post:
                    return redirect('detail', title=post.title)
            count = count + 1
            com.note = post
            com.user = request.user
            com.save()
            return redirect('detail', title=post.title)
        elif request.POST.get("form_type") == 'formTwo':
            if form.is_valid():
                com = form.save(commit=False)
                com.note = post
                com.user = request.user
                com.save()
                return redirect('detail', title=post.title)
            else:
                form = CommentModelForm()
    template = 'note/detail.html'
    context = {
        'form': form,
        'norm': norm,
        'post': post,
        'count': count
    }
    return render(request, template, context)


class PersonalView(TemplateView):
    template_name = 'note/personal.html'

    def get(self, request, *args, **kwargs):
        q = NoteModel.objects.all()
        context = {
            'q': q
        }
        return render(request, self.template_name, context)


class SortView(TemplateView):
    template_name = 'note/sort.html'

    def get(self, request, *args, **kwargs):
        value = self.request.GET.get('sort')
        if value == 'date':
            q = NoteModel.objects.order_by('date')
        else:
            q = NoteModel.objects.order_by('categories')
        context = {
            'q': q
        }
        return render(request, self.template_name, context)

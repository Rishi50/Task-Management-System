from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction
from django.utils import timezone
from .models import Task,tasklist
from .forms import PositionForm, todo_task

from .forms import CustomUserCreationForm
from .forms import UpdateUserForm, UpdateProfileForm
@login_required
def logoutuser(request):
    if request.method =='POST':
        logout(request)
        return redirect(home)

def home(request):
    return render(request, 'base/home.html')

# @login_required
# def profile(request):
#     return render(request, 'base/profile.html')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'base/profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'base/createtodo.html',{'form':todo_task})
    else:
        try:
            form = todo_task(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'base/createtodo.html',{'form':todo_task,'error':'value exceed'})

def currenttodos(request):
    todos = tasklist.objects.filter(user = request.user,datecompleted__isnull=True)
    return render(request, 'base/currenttodos.html',{'todos':todos})


def completedtodo(request):
    todo = tasklist.objects.filter(user = request.user,datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'base/completedtodos.html',{'todos':todo})

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'base/createtodo.html',{'form':todo_task})
    else:
        try:
            form = todo_task(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'base/createtodo.html',{'form':todo_task,'error':'value exceed'})


def viewtodo(request,todo_pk):
    todos = get_object_or_404(tasklist,pk=todo_pk,user=request.user)
    if request.method =='GET':
        todoform = todo_task(instance=todos)
        return render(request, 'base/viewtodo.html',{'todo':todos,'form':todoform})
    else:
        try:
            form = todo_task(request.POST,instance=todos)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'base/viewtodo.html',{'todos':todos,'form':todoform,'error':'value error'})


def completetodo(request,todo_pk):
    todos = get_object_or_404(tasklist,pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todos.datecompleted = timezone.now()
        todos.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request,todo_pk):
    todos = get_object_or_404(tasklist,pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todos.delete()
        return redirect('currenttodos')

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


# class RegisterPage(FormView):
#     template_name = 'base/register.html'
#     form_class = UserCreationForm()
#     redirect_authenticated_user = True
#     success_url = reverse_lazy('tasks')

#     def form_valid(self, form):
#         user = form.save()
#         if user is not None:
#             login(self.request, user)
#         return super(RegisterPage, self).form_valid(form)

#     def get(self, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             return redirect('tasks')
#         return super(RegisterPage, self).get(*args, **kwargs)


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'base/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user to the database
            return redirect(reverse_lazy('login'))  # Redirect to login page after successful registration
        return render(request, 'base/register.html', {'form': form})



class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'base/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')
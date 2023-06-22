
from django.shortcuts import render,redirect
from .models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CustomLoginForm


class Register(FormView):
    template_name = 'App/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(Register,self).form_valid(form)
    
    #to restrict already logged in user to access login page
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(Register,self).get(*args, **kwargs)

class CustomLoginView(LoginView):
    template_name='App/login.html'
    form_class = CustomLoginForm
    fields = '__all__'
    redirect_authenticated_user= True
    
    def get_redirect_url(self):
        return reverse_lazy('tasks')
    

@method_decorator(login_required,name='dispatch')
class TaskList(ListView):
    model = Task
    context_object_name ='tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
            context['search_input']=search_input
        return context    

@method_decorator(login_required,name='dispatch')
class TaskDetail(DetailView):
    model = Task
    context_object_name= 'task'

@method_decorator(login_required,name='dispatch')
class TaskCreate(CreateView):
    model= Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')


    #form_valid method automatically saves task to the database
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

@method_decorator(login_required,name='dispatch')
class TaskUpdate(UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

@method_decorator(login_required,name='dispatch')
class TaskDelete(DeleteView):
    model = Task
    context_object_name ='task'
    success_url = reverse_lazy('tasks')
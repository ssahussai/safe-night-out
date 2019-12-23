from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import DrinkSession, Drink, Profile

# Create your views here.
class DrinksessionCreate(CreateView):
  model = DrinkSession
  fields = ['start_time', 'duration']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class DrinksessionUpdate(UpdateView):
  model = DrinkSession
  fields = ['start_time']

class DrinksessionDelete(DeleteView):
  model = DrinkSession
  success_url = '/drinksessions/'

def home(request):
    p = Profile.objects.all()
    return render(request, 'home.html', {'profile':p})

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def drinksession_index(request):
  session = DrinkSession.objects.all()
  return render(request, 'drinksessions/index.html', {'session':session})

def drinksession_detail(request, session_id):
  return render(request, 'drinksessions/detail.html', {'session': DrinkSession.objects.get(id=session_id) })

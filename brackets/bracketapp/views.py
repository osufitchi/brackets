from models import Bracket, Competitor
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from django.contrib.auth.views import login
from django.views.generic import CreateView, UpdateView, FormView
from django.utils.decorators import method_decorator

class RichUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label = "First name")
    last_name = forms.CharField(label = "Last name")
    email = forms.EmailField(label = "Email")

    def save(self, commit=True):
        user = super(RichUserCreationForm, self).save(commit=False)
        first_name =self.cleaned_data["first_name"]
        last_name =self.cleaned_data["last_name"]
        email =self.cleaned_data["email"]
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        if commit:
            user.save()
        return user

def register(request):
    if request.method == 'POST':
           form = RichUserCreationForm(request.POST)
           if form.is_valid():
               new_user = form.save()
               return HttpResponseRedirect("/login/")
    else:
           form = RichUserCreationForm()
    return render_to_response("registration/register.html", {
        'form': form,
    },context_instance=RequestContext(request))


class BracketCreateView(CreateView):
    model = Bracket
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BracketCreateView, self).dispatch(*args, **kwargs)
    def form_valid(self,form):
        self.object = form.save()
        competitor = Competitor(name="Default Name", bracket=self.object)
        for person in range(self.object.maxnum):
            competitor.pk = None
            competitor.save()
        return super(BracketCreateView, self).form_valid(form)

class CompetitorForm(forms.Form):
   def __init__(self,fields, *args, **kwargs):
       super(CompetitorForm,self).__init__(*args,**kwargs)
       for i in xrange(fields):
           self.fields['competitor_%i' % i] = forms.CharField()

class BracketModify(FormView):
    form_class = CompetitorForm
    template_name = "modify.html" 
    def get_form_kwargs(self):
       kwargs = super(BracketModify,self).get_form_kwargs()
       kwargs.update({"fields":Bracket.objects.get(id=self.kwargs['pk']).maxnum})
       return kwargs
    def get_success_url(self):
        return "/bracket/%i" % int(self.kwargs["pk"])


    

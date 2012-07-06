from bracket.models import Bracket, Competitor, Competition
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm

class RichUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label = "First name")
    last_name = forms.CharField(label = "Last name")
    
    def save(self, commit=True):
        user = super(RichUserCreationForm, self).save(commit=False)
        first_name =self.cleaned_data["first_name"]
        last_name =self.cleaned_data["last_name"]
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



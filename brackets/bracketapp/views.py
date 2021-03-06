from models import Bracket, Competitor, Competition
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from django.contrib.auth.views import login
from django.views.generic import CreateView, UpdateView, FormView, DetailView, ListView
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

class BracketForm(forms.ModelForm):
    class Meta:
        model = Bracket
        exclude = ("tourny_round")

class BracketCreateView(CreateView):
    model = Bracket
    form_class =  BracketForm
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BracketCreateView, self).dispatch(*args, **kwargs)
    def form_valid(self,form):
        self.object = form.save()
        competitor = Competitor(name="Default Name", bracket=self.object)
        seeds = xrange(self.object.maxnum)
        for person in range(self.object.maxnum):
            competitor.pk = None
            competitor.seed = person
            competitor.save()
        for i  in  range(self.object.maxnum / 2 ):
            comp = Competition(bracket=self.object,competitor_a=Competitor.objects.get(bracket=self.object,seed=seeds[2 * i]),competitor_b=Competitor.objects.get(bracket=self.object,seed=seeds[2 * i + 1]))
            comp.save()
        return super(BracketCreateView, self).form_valid(form)

class CompetitorForm(forms.Form):
   def __init__(self,fields, *args, **kwargs):
       super(CompetitorForm,self).__init__(*args,**kwargs)
       for i in xrange(fields):
           self.fields['Seed_%i' % i] = forms.CharField()


class WinnerForm(forms.Form):

   def __init__(self,*args,**kwargs):
       self.competition = Competition.objects.get(id=kwargs.pop("competition"))
       super(WinnerForm,self).__init__(*args,**kwargs)
       combined_list  = set([self.competition.competitor_a.pk,self.competition.competitor_b.pk]) 
       self.fields['winner']= forms.ModelChoiceField(queryset=Competitor.objects.filter(pk__in = combined_list))


class BracketDetailView(DetailView):
    def get_context_data(self,**kwargs):
        context = super(BracketDetailView,self).get_context_data(**kwargs)
        num_rounds = 3
        for round in range(num_rounds):
            comps = Competition.objects.filter(bracket=self.object.id, tourny_round=round+1)
            for index, comp in enumerate(comps):
                key = 'comp_%s_%s' % (round + 1, index + 1)
                context[key] = comp
        for seed in xrange(self.object.maxnum):
            context["seed_%i" % seed] = self.object.competitor_set.get(seed=seed)
        return context


class BracketModify(FormView):
    form_class = CompetitorForm
    template_name = "modify.html"
    def get_form_kwargs(self):
       kwargs = super(BracketModify,self).get_form_kwargs()
       kwargs.update({"fields":Bracket.objects.get(id=self.kwargs['pk']).maxnum})
       
       return kwargs
    def get_initial(self):
        initial = {}
        fields = Bracket.objects.get(id=self.kwargs['pk']).maxnum
        for i in xrange(fields):
           initial['Seed_%i' % i] = Bracket.objects.get(id=self.kwargs['pk']).competitor_set.get(seed=i)
        return initial
    def form_valid(self,form):
        for seed in xrange(Bracket.objects.get(id=self.kwargs['pk']).maxnum):
            comp = Competitor.objects.get(bracket=self.kwargs["pk"],seed= seed)
            comp.name = form.cleaned_data["Seed_%i" % seed]
            comp.save()
        return super(BracketModify,self).form_valid(form)
    def get_success_url(self):
        return "/bracket/%i" % int(self.kwargs["pk"])

def winner_form(request,pk,competition):
    if request.method == "POST":
        form = WinnerForm(request.POST,competition=competition)
        if form.is_valid():
          comp =  Competition.objects.get(id=competition)
          comp.winner = form.cleaned_data['winner']
          comp.save()
          check_bracket_round_complete(pk)
          return HttpResponseRedirect('/')
        
    else:
        form = WinnerForm(competition=competition)
    return render_to_response('herpderp.html',{'form':form},RequestContext(request))


class UnresolvedCompetitionListView(ListView):
    def dispatch(self, request, *args, **kwargs):
        bracket = Bracket.objects.get(id=kwargs['pk'])
        self.queryset = Competition.objects.filter(bracket = kwargs['pk'], tourny_round=bracket.tourny_round,winner=None)
        return super(UnresolvedCompetitionListView, self).dispatch(request,*args, **kwargs)

def zigzag(seq):
  results = []
  for i, e in enumerate(seq):
    results.append((i,e))
  return results

def check_bracket_round_complete(bracket):
    if Competition.objects.filter(bracket = bracket,winner=None):
        pass
    else:
        br = Bracket.objects.get(id=bracket)
        br.tourny_round += 1 
        br.save()
        compnum = Competition.objects.filter(bracket = br.id, tourny_round=br.tourny_round - 1).count()  / 2

        #obvious bug here, try to fix it at some point
        # hint: it's only a problem if more then one person is using the site at a time ~~ hey are you there?? :(
        winnerlist = Competition.objects.values_list('winner',flat=True).filter(tourney_round = br.tourney_round - 1).exclude(winner=None).order_by('id')
        players=zigzag(winnerlist)

        for player_a, player_b in players:
            comp = Competition(bracket = br, tourny_round = br.tourny_round,commit = False)
            comp.competitor_a = player_a
            comp.competitor_b = player_b
            comp.save()

            
        

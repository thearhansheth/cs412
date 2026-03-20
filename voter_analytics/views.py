# File: voter_analytics/views.py
# Author: Arhan Sheth, 3/20/2026
# Email: aksheth@bu.edu
# Description: views.py for Voter Analytics

from django.shortcuts import render
from django.views.generic import ListView, DetailView
import plotly
from collections import Counter
import plotly.graph_objects as go
from plotly.offline import plot
from plotly.colors import qualitative
from django.db.models import Count
from .models import Voter

# Create your views here.
class VotersListView(ListView):
    """View to display voter results
    """
 
    template_name = 'voter_analytics/results.html'
    model = Voter
    context_object_name = 'results'
    paginate_by = 100
 
    def get_queryset(self):
        
        # start with entire queryset
        results = super().get_queryset().order_by('last_name', 'first_name')


        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        #filter results
        if party:
            results = results.filter(party__iexact=party.strip())

        if min_dob:
          results = results.filter(dob__year__gte=int(min_dob))

        if max_dob:
            results = results.filter(dob__year__lte=int(max_dob))

        if voter_score:
            results = results.filter(voter_score=voter_score)

        # for each election checkbox, filter to voters who participated if checked
        for field in ['v20', 'v21town', 'v21primary', 'v22', 'v23']:
            if self.request.GET.get(field):
                results = results.filter(**{field: True})

        return results
    

    def get_context_data(self, **kwargs):
        """Override the built in get_context_data to populate fields.
        """
        context = super().get_context_data(**kwargs)
        get_copy = self.request.GET.copy()

        if 'page' in get_copy:
            del get_copy['page']

        context['query_string'] = get_copy.urlencode()
        context['parties'] = Voter.objects.values_list('party', flat=True).distinct().order_by('party')
        context['years'] = range(1900, 2007)
        context['scores'] = range(0, 6)
        context['get'] = self.request.GET       # used to re-select form values after submit

        return context
      

class VoterDetailView(DetailView):
    """View for handling a single instance of a voter's details.
    """
    template_name = 'voter_analytics/voter.html'
    model = Voter
    context_object_name = 'voter'
    

class GraphListView(ListView):
    """View for displaying graphs of voter data.
    """
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'


    def get_queryset(self):
        """Returns filtered queryset based on GET parameters.
        Mirrors the filtering logic in VotersListView.
        """
        queryset = Voter.objects.all()

        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        if party:
            queryset = queryset.filter(party=party)
        if min_dob:
            queryset = queryset.filter(dob__year__gte=int(min_dob))
        if max_dob:
            queryset = queryset.filter(dob__year__lte=int(max_dob))
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)

        # only include voters who participated in each checked election
        for field in ['v20', 'v21town', 'v21primary', 'v22', 'v23']:
            if self.request.GET.get(field):
                queryset = queryset.filter(**{field: True})

        return queryset


    def get_context_data(self, **kwargs):
        """Override get_context_data to add graphs and form choices.
        """
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        # form context
        context['parties'] = Voter.objects.values_list('party', flat=True).distinct().order_by('party')
        context['years'] = range(1900, 2007)
        context['scores'] = range(0, 6)
        context['get'] = self.request.GET

        # Graph 1: Birth Year Histogram
        # extract birth years from voters who have a valid dob
        years = [v.dob.year for v in voters if v.dob]
        year_counts = Counter(years)
        fig_birth = go.Figure(data=[go.Bar(
            x=list(year_counts.keys()),
            y=list(year_counts.values())
        )])

        fig_birth.update_layout(
            title="Distribution of Voters by Year of Birth",
            xaxis_title="Year of Birth",
            yaxis_title="Number of Voters"
        )
        context['graph_birth'] = plotly.offline.plot(fig_birth, auto_open=False, output_type="div")

        # Graph 2: Party Affiliation Pie Chart
        # use 'Unknown' for any voter with no party on record
        parties = [v.party if v.party else 'Unknown' for v in voters]
        party_counts = Counter(parties)
        fig_party = go.Figure(data=[go.Pie(
            labels=list(party_counts.keys()),
            values=list(party_counts.values()),
            marker=dict(colors=qualitative.Set3)
        )])

        fig_party.update_layout(title="Distribution of Voters by Party Affiliation")
        context['graph_party'] = plotly.offline.plot(fig_party, auto_open=False, output_type="div")

        # Graph 3: Election Participation Histogram
        election_fields = ['v20', 'v21town', 'v21primary', 'v22', 'v23']
        participation_counts = {field: 0 for field in election_fields}

        for v in voters:
            for field in election_fields:
                if getattr(v, field):
                    participation_counts[field] += 1

        fig_participation = go.Figure(data=[go.Bar(
            x=list(participation_counts.keys()),
            y=list(participation_counts.values())
        )])
        
        fig_participation.update_layout(
            title="Voter Participation Across Elections",
            xaxis_title="Election",
            yaxis_title="Number of Voters"
        )
        context['graph_participation'] = plotly.offline.plot(fig_participation, auto_open=False, output_type="div")

        return context
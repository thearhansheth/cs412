# File: project/views.py
# Author: Arhan Sheth, 4/28/2026
# Email: aksheth@bu.edu
# Description: views.py for the Job Application Tracker

from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import json
from django.db.models import Count, Q
 
from .models import Company, JobPosting, Application, Contact
from .forms import CompanyForm, JobPostingForm, ApplicationForm, ContactForm


# Create your views here.
@login_required(login_url='login')
def dashboard_view(request):
    """Display the dashboard with analytics, kanban, and sankey visualizations
    """
    # restrict applications to those belonging to the current user only
    user_applications = Application.objects.filter(user=request.user)
 
    # build the kanban pipeline as a list of stage dicts for the toggle view
    pipeline = []
    for status_code, status_label in Application.STATUS_CHOICES:
        apps_in_stage = user_applications.filter(status=status_code)
        pipeline.append({
            'code': status_code,
            'label': status_label,
            'applications': apps_in_stage,
            'count': apps_in_stage.count(),
        })

    # used Django ORM aggregation to compute analytics in a single query.
    # Q-filtered Count expressions give per-status counts efficiently.
    analytics = user_applications.aggregate(
        n_submitted=Count('id', filter=~Q(status='wishlist')),
        n_responded=Count('id', filter=~Q(status__in=['wishlist', 'applied'])),
        n_interviewed=Count('id', filter=Q(status__in=['interview', 'final_round', 'offer'])),
        n_offers=Count('id', filter=Q(status='offer')),
        n_rejected=Count('id', filter=Q(status='rejected')),
    )
 
    # compute conversion rates as percentages, guarding against division-by-zero
    n_submitted = analytics['n_submitted'] or 0
    response_rate = round(analytics['n_responded'] / n_submitted * 100, 1) if n_submitted else 0
    interview_rate = round(analytics['n_interviewed'] / n_submitted * 100, 1) if n_submitted else 0
    offer_rate = round(analytics['n_offers'] / n_submitted * 100, 1) if n_submitted else 0
 
    # build the Sankey diagram data showing pipeline flow.
    # cumulative counts: an app at "interview" implicitly passed through earlier stages
    stage_order = ['applied', 'phone_screen', 'interview', 'final_round', 'offer']
    n_at_stage = {}
    for i, stage in enumerate(stage_order):
        # count apps at this stage OR any later stage
        n_at_stage[stage] = user_applications.filter(status__in=stage_order[i:]).count()
 
    # build the Sankey flow arrays for a linear progression funnel.
    # rejection is shown as a separate stat rather than a flow node, since
    # we don't track which stage rejection occurred at. modeling rejection
    # as a single flow off "Applied" produces visually misleading layouts
    # at scale (long crossing ribbons), so we keep the funnel pure.
    sankey_labels = ['Applied', 'Phone Screen', 'Interview', 'Final Round', 'Offer']
    sankey_sources, sankey_targets, sankey_values = [], [], []

    # linear pipeline progression: each transition uses the cumulative count
    if n_at_stage['phone_screen'] > 0:
        sankey_sources.append(0)
        sankey_targets.append(1)
        sankey_values.append(n_at_stage['phone_screen'])
    if n_at_stage['interview'] > 0:
        sankey_sources.append(1)
        sankey_targets.append(2)
        sankey_values.append(n_at_stage['interview'])
    if n_at_stage['final_round'] > 0:
        sankey_sources.append(2)
        sankey_targets.append(3)
        sankey_values.append(n_at_stage['final_round'])
    if n_at_stage['offer'] > 0:
        sankey_sources.append(3)
        sankey_targets.append(4)
        sankey_values.append(n_at_stage['offer'])
 
    context = {
        # kanban pipeline
        'pipeline': pipeline,
 
        # summary statistics shown in the top stat cards
        'total_applications': user_applications.count(),
        'total_companies': Company.objects.count(),
        'total_postings': JobPosting.objects.count(),
 
        # analytics for the conversion-rate cards
        'n_submitted': n_submitted,
        'n_responded': analytics['n_responded'],
        'n_interviewed': analytics['n_interviewed'],
        'n_offers': analytics['n_offers'],
        'n_rejected': analytics['n_rejected'],
        'response_rate': response_rate,
        'interview_rate': interview_rate,
        'offer_rate': offer_rate,
 
        # sankey diagram data, JSON-encoded for safe inclusion in JS
        'sankey_labels': json.dumps(sankey_labels),
        'sankey_sources': json.dumps(sankey_sources),
        'sankey_targets': json.dumps(sankey_targets),
        'sankey_values': json.dumps(sankey_values),
    }
    
    return render(request, 'project/dashboard.html', context)


class SignUpView(CreateView):
    """Allow new users to create an account, then auto-login on success
    """
    form_class = UserCreationForm
    template_name = 'project/signup.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        """Save the new user and log them in immediately
        """
        # save via the parent CreateView, then call login() on the new user
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


# Company views: CRUD for the Company model

class CompanyListView(LoginRequiredMixin, ListView):
    """Display a list of all companies
    """
    model = Company
    template_name = 'project/company_list.html'
    context_object_name = 'companies'


class CompanyDetailView(LoginRequiredMixin, DetailView):
    """Display details of a single company
    """
    model = Company
    template_name = 'project/company_detail.html'
    context_object_name = 'company'


class CompanyCreateView(LoginRequiredMixin, CreateView):
    """Allow users to create a new company record
    """
    model = Company
    form_class = CompanyForm
    template_name = 'project/company_form.html'

    def get_success_url(self):
        """Redirect to the new company's detail page after creation
        """
        return reverse('company_detail', kwargs={'pk': self.object.pk})


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    """Allow users to update an existing company record
    """
    model = Company
    form_class = CompanyForm
    template_name = 'project/company_form.html'

    def get_success_url(self):
        """Redirect to the updated company's detail page
        """
        return reverse('company_detail', kwargs={'pk': self.object.pk})


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    """Allow users to delete a company record after confirmation
    """
    model = Company
    template_name = 'project/company_confirm_delete.html'
    success_url = reverse_lazy('company_list')


# JobPosting views: CRUD for the JobPosting model

class JobPostingListView(LoginRequiredMixin, ListView):
    """Display a list of all job postings
    """
    model = JobPosting
    template_name = 'project/job_posting_list.html'
    context_object_name = 'job_postings'


class JobPostingDetailView(LoginRequiredMixin, DetailView):
    """Display details of a single job posting
    """
    model = JobPosting
    template_name = 'project/job_posting_detail.html'
    context_object_name = 'job_posting'


class JobPostingCreateView(LoginRequiredMixin, CreateView):
    """Allow users to create a new job posting
    """
    model = JobPosting
    form_class = JobPostingForm
    template_name = 'project/job_posting_form.html'

    def get_success_url(self):
        """Redirect to the new posting's detail page after creation
        """
        return reverse('job_posting_detail', kwargs={'pk': self.object.pk})


class JobPostingUpdateView(LoginRequiredMixin, UpdateView):
    """Allow users to update an existing job posting
    """
    model = JobPosting
    form_class = JobPostingForm
    template_name = 'project/job_posting_form.html'

    def get_success_url(self):
        """Redirect to the updated posting's detail page
        """
        return reverse('job_posting_detail', kwargs={'pk': self.object.pk})


class JobPostingDeleteView(LoginRequiredMixin, DeleteView):
    """Allow users to delete a job posting after confirmation
    """
    model = JobPosting
    template_name = 'project/job_posting_confirm_delete.html'
    success_url = reverse_lazy('job_posting_list')


# Application views: CRUD for the Application model.
# Application data is private to each user, so list/detail/update/delete
# all restrict the queryset to the logged-in user's records only.

class ApplicationListView(LoginRequiredMixin, ListView):
    """Display the user's applications, with optional status/company filters
    """
    model = Application
    template_name = 'project/application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        """Return only the current user's applications, optionally filtered
        """
        # always restrict to the current user's own data for privacy
        queryset = Application.objects.filter(user=self.request.user)
 
        # if status filter is supplied via GET params, narrow further
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
 
        # if company filter is supplied, narrow by FK lookup through job_posting
        company_id = self.request.GET.get('company')
        if company_id:
            queryset = queryset.filter(job_posting__company__id=company_id)
 
        return queryset.order_by('-date_applied')

    def get_context_data(self, **kwargs):
        """Add filter dropdown options and current selections to context
        """
        context = super().get_context_data(**kwargs)
 
        # provide options for the filter dropdown form
        context['status_choices'] = Application.STATUS_CHOICES
        context['companies'] = Company.objects.all()
 
        # echo current filter selections back so the form remembers them
        context['current_status'] = self.request.GET.get('status', '')
        context['current_company'] = self.request.GET.get('company', '')
        return context


class ApplicationDetailView(LoginRequiredMixin, DetailView):
    """Display details of a single application owned by the current user
    """
    model = Application
    template_name = 'project/application_detail.html'
    context_object_name = 'application'

    def get_queryset(self):
        """Restrict access to the current user's own applications
        """
        # privacy: prevent users from viewing each other's applications
        return Application.objects.filter(user=self.request.user)


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    """Allow users to create a new application record
    """
    model = Application
    form_class = ApplicationForm
    template_name = 'project/application_form.html'

    def form_valid(self, form):
        """Set the application's user to the current user before saving
        """
        # the form does not expose the user FK, so we set it here
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the new application's detail page after creation
        """
        return reverse('application_detail', kwargs={'pk': self.object.pk})


class ApplicationUpdateView(LoginRequiredMixin, UpdateView):
    """Allow users to update one of their own applications
    """
    model = Application
    form_class = ApplicationForm
    template_name = 'project/application_form.html'

    def get_queryset(self):
        """Restrict updates to the current user's own applications
        """
        # users may only update their own applications, never others'
        return Application.objects.filter(user=self.request.user)

    def get_success_url(self):
        """Redirect to the updated application's detail page
        """
        return reverse('application_detail', kwargs={'pk': self.object.pk})


class ApplicationDeleteView(LoginRequiredMixin, DeleteView):
    """Allow users to delete one of their own applications
    """
    model = Application
    template_name = 'project/application_confirm_delete.html'
    success_url = reverse_lazy('application_list')

    def get_queryset(self):
        """Restrict deletes to the current user's own applications
        """
        # users may only delete their own applications, never others'
        return Application.objects.filter(user=self.request.user)


# Contact views: CRUD for the Contact model

class ContactListView(LoginRequiredMixin, ListView):
    """Display a list of all professional contacts
    """
    model = Contact
    template_name = 'project/contact_list.html'
    context_object_name = 'contacts'


class ContactDetailView(LoginRequiredMixin, DetailView):
    """Display details of a single contact
    """
    model = Contact
    template_name = 'project/contact_detail.html'
    context_object_name = 'contact'


class ContactCreateView(LoginRequiredMixin, CreateView):
    """Allow users to create a new contact record
    """
    model = Contact
    form_class = ContactForm
    template_name = 'project/contact_form.html'

    def get_success_url(self):
        """Redirect to the new contact's detail page after creation
        """
        return reverse('contact_detail', kwargs={'pk': self.object.pk})


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    """Allow users to update an existing contact record
    """
    model = Contact
    form_class = ContactForm
    template_name = 'project/contact_form.html'

    def get_success_url(self):
        """Redirect to the updated contact's detail page
        """
        return reverse('contact_detail', kwargs={'pk': self.object.pk})


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    """Allow users to delete a contact record after confirmation
    """
    model = Contact
    template_name = 'project/contact_confirm_delete.html'
    success_url = reverse_lazy('contact_list')

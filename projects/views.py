from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView

from django.http import HttpResponseRedirect
from django.http import HttpResponse

from .forms import RequirementForm, ProjectForm
from .models import Project, Profile, ProjectView, Requirement, RequirementCategory
from .utils import render_to_pdf
from account.models import Signup, Account


def get_profile(user):
    qs = Profile.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


class SearchProjectProfileView(ListView):
    model = Project
    template_name = 'search_project_profile.html'
    context_object_name = 'queryset'
    ordering = ['-created']
    paginate_by = 4

    def get(self, request, *args, **kwargs):
        queryset = Project.objects.all()
        query = get_profile(self.request.user)
        
        if query:
            queryset = queryset.filter(
                Q(profile__user__username=query))
        context = {
            'queryset': queryset,
        }
        return render(request, 'search_project_profile.html', context)


class SearchView(ListView):
    model = Project
    template_name = 'search_results.html'
    context_object_name = 'queryset'
    ordering = ['-created']
    paginate_by = 4

    def get(self, request, *args, **kwargs):
        queryset = Project.objects.all()
        query = request.GET.get('q')
        category_count = get_category_count()
        most_recent = Project.objects.order_by('-created')[:3]
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(overview__icontains=query)
            ).distinct()
        context = {
            'queryset': queryset,
            'most_recent' : most_recent,
            'page_request_var' : "page",
            'category_count' : category_count
        }
        return render(request, 'search_results.html', context)


class SearchCategorieView(ListView):
    model = Project
    template_name = 'search_results.html'
    context_object_name = 'queryset'
    ordering = ['-created']
    paginate_by = 4

    def get(self, request, *args, **kwargs):
        queryset = Project.objects.all()
        query = request.GET.get('q')
        category_count = get_category_count()
        most_recent = Project.objects.order_by('-created')[:3]
        
        if query:
            queryset = queryset.filter(
                Q(categories__title=query))
        context = {
            'queryset': queryset,
            'most_recent' : most_recent,
            'page_request_var' : "page",
            'category_count' : category_count
        }
        return render(request, 'search_results.html', context)


def get_category_count():
    queryset = Project \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset

class ProjectListView(ListView):
    model = Project
    template_name = 'blog.html'
    context_object_name = 'queryset'
    ordering = ['-created']
    paginate_by = 4

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Project.objects.order_by('-created')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project.html'
    context_object_name = 'project'
    form_req = RequirementForm()

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            ProjectView.objects.get_or_create(
                user=self.request.user,
                project=obj
            )
        return obj

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Project.objects.order_by('-created')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form_req'] = self.form_req
        return context

    def post(self, request, *args, **kwargs):
        form = RequirementForm(request.POST)
        if form.is_valid():
            project = self.get_object()
            form.instance.user = request.user
            form.instance.project = project
            form.save()
            return redirect(reverse("project-detail", kwargs={
                'pk': project.pk
            }))
   

class ProjectCreateView(CreateView):
    model = Project
    template_name = 'project_create.html'
    form_class = ProjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Posting a Project'
        return context

    def form_valid(self, form):
        form.instance.profile = get_profile(self.request.user)
        form.save()
        return redirect(reverse("project-detail", kwargs={
            'pk': form.instance.pk
        }))


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'project_create.html'
    form_class = ProjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Project'
        return context

    def form_valid(self, form):
        form.instance.profile = get_profile(self.request.user)
        form.save()
        return redirect(reverse("project-detail", kwargs={
            'pk': form.instance.pk
        }))


def get_pdf(request, pk):
    uid = Project.objects.get(id__iexact=pk)
    q = Requirement.objects.filter(project=pk)
    if q.exists():
        print("id exist")
        print(q)
        qn = q.filter(status='A')
        if qn.exists():
            print("ini adalah approved requirement : ")        
            print(qn)
        data = {
            'queryset': qn,
            'title' : uid.title,
            'object': uid
        }
        pdf = render_to_pdf('pdf/report.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        return HttpResponse('<h1>Invalid report link</h1>')

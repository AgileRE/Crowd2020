from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView

from django.http import HttpResponseRedirect
from django.http import HttpResponse

from .forms import RequirementForm, ProjectForm
from .models import Project, Profile, ProjectView, Requirement
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
    paginate_by = 4

    def get(self, request, *args, **kwargs):
        queryset = Project.objects.all()
        query = get_profile(self.request.user)
        
        if query:
            queryset = queryset.filter(profile__user__username=query).order_by('-created')
        context = {
            'queryset': queryset,
        }
        return render(request, 'search_project_profile.html', context)


class SearchProjectContributionView(ListView):
    model = Project
    template_name = 'search_project_contribution.html'
    context_object_name = 'queryset'
    paginate_by = 4

    def get(self, request, *args, **kwargs):
        queryset = Project.objects.all()
        query = get_profile(self.request.user)
        requirement = Requirement.objects.filter(user__username=query).values('project').distinct()

        if query:
            queryset = queryset.filter(pk__in=requirement).order_by('-created')
            print(queryset)
        context = {
            'queryset': queryset,
        }
        return render(request, 'search_project_contribution.html', context)


class SearchView(ListView):
    model = Project
    template_name = 'search_results.html'
    context_object_name = 'queryset'
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
            ).distinct().order_by('-created')
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
    paginate_by = 4

    def get(self, request, *args, **kwargs):
        queryset = Project.objects.all()
        query = request.GET.get('q')
        category_count = get_category_count()
        most_recent = Project.objects.order_by('-created')[:3]
        
        if query:
            queryset = queryset.filter(
                Q(categories__title=query)).order_by('-created')
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
        project = super().get_object()
        category_count = get_category_count()
        most_recent = Project.objects.order_by('-created')[:3]
        is_liked = False
        if project.likes.filter(id=self.request.user.id).exists():
            is_liked=True

        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form_req'] = self.form_req
        context['is_liked'] = is_liked
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


class RequirementDeleteView(DeleteView):
    model = Requirement
    template_name = 'requirement_confirm_delete.html'

    def get_success_url(self):
        # Assuming there is a ForeignKey from Comment to Post in your model
        requirement = self.get_object() 
        return reverse( 'project-detail', kwargs={
            'pk': requirement.project.id
            })

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Project.objects.order_by('-created')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        return context


def get_pdf(request, pk, slug):
    uid = Project.objects.get(slug__iexact=slug)
    q = Requirement.objects.filter(project=pk)
    if uid:
        if q.exists():
            qn = q.filter(status='A')
            data = {
                'queryset': qn,
                'title' : uid.title,
                'overview' : uid.overview,
                'object': uid,
                'created' : uid.created,
                'updated' : uid.updated,
                'slug' : uid.slug
            }
        else:
            data = {
                'title' : uid.title,
                'overview' : uid.overview,
                'object': uid,
                'created' : uid.created,
                'updated' : uid.updated,
                'slug' : uid.slug
            }
        pdf = render_to_pdf('pdf/report.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        return HttpResponse('<h1>Invalid report link</h1>')


def like_project(request, id):
    project = get_object_or_404(Project,id=id)
    if project.likes.filter(id=request.user.id).exists():
        project.likes.remove(request.user)
    else:
        project.likes.add(request.user)
    return HttpResponseRedirect(project.get_absolute_url())


def like_project_list(request):
    user = request.user
    like_projects = user.likes.all().order_by('-created')
    context = {
        'queryset' : like_projects
    }
    return render(request, 'search_project_likes.html', context)

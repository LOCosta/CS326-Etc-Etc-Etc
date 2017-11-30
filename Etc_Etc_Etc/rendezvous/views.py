from django.shortcuts import render
from .models import Skill, Tag, Event, Location, Profile, Project
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView
import datetime
from .forms import ProjectForm, ProfileForm


def profile(request, id):
    """
    View function for the profile page.
    """
    user = Profile.objects.get(id=id)
    user_name = user.name
    user_skills = user.relevant_skills.all()

    proj_created = user.projects_owned.order_by('-date_created')
    num_proj_created = proj_created.count()

    proj_contributed = user.project_set.all()
    num_proj_contributed = proj_contributed.count()

    return render(
        request, 'profile.html',
        context={'user_name': user_name, 'user_skills': user_skills, 'proj_created': proj_created,
                 'num_proj_created': num_proj_created, 'proj_contributed': proj_contributed,
                 'num_proj_contributed': num_proj_contributed, 'id': id}
    )


def project(request, id):
    """
    View function for the project page.
    """
    project = Project.objects.get(id=id)
    proj_name = project.name
    proj_creator = project.owner
    proj_description = project.description
    proj_contributors = project.contributors.all()
    skills_desired = project.skills_desired.all()

    return render(
        request, 'project.html',
        context={'proj_name': proj_name, 'proj_creator': proj_creator, 'proj_description': proj_description,
                 'proj_contributors': proj_contributors, 'skills_desired': skills_desired}
    )


def index(request):
    return render(
        request, 'index.html',
        context={}
    )


def search(request):
    """
    View function for advanced search page.
    """
    skills = Skill.objects.all()

    return render(
        request,
        'search.html',
        context={'skills': skills},
    )

def search_review(request):
    """
    View function for advanced search page.
    """

    projects = Project.objects.all()[:12]  # Load only up to 12 results for now, need more once search is implemented
    result_rows = [projects[0:4], projects[4:8], projects[8:12]]  # Also temporary.

    return render(
        request,
        'search.html',
        context={'result_rows': result_rows},
    )


class ProjectListView(generic.ListView):
    model = Project
    context_object_name = 'project_list'
    template_name = 'project_list.html'


class ProfileListView(generic.ListView):
    model = Profile
    context_object_name = 'user_list'
    template_name = 'user_list.html'

# @login_required
# def create_project(request):
#     if request.method == 'POST':
#         form = CreateProjectForm(request.POST)
#         if form.is_valid():
#
#             return HttpResponseRedirect(reverse('view-project', '2'))
#     else:
#         form = CreateProjectForm()
#     return render(request, 'create-a-new-project-post.html', {'form': form})


class ProjectCreate(CreateView, LoginRequiredMixin):
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('view-project', args=(self.object.id.hex,))

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        form.instance.date_created = datetime.date.today()
        return super(ProjectCreate, self).form_valid(form)


class ProjectUpdate(UpdateView):
    model = Project
    form_class = ProjectForm


class ProfileUpdate(UpdateView):
    model = Profile
    form_class = ProfileForm
from django.shortcuts import render
from .models import Skill, Tag, Event, Location, User, Project
from django.views import generic


def profile(request, id):
    """
    View function for the profile page.
    """
    user = User.objects.get(id=id)
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
                 'num_proj_contributed': num_proj_contributed}
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


def create_project(request):
    skills = Skill.objects.all()
    return render(
        request, 'create-a-new-project-post.html',
        context={'skills': skills}
    )


def search(request):
    """
    View function for advanced search page.
    """

    projects = Project.objects.all()[:12]  # Load only up to 12 results for now, need more once search is implemented
    skills = Skill.objects.all()
    result_rows = [projects[0:4], projects[4:8], projects[8:12]]  # Also temporary.

    return render(
        request,
        'search.html',
        context={'result_rows': result_rows, 'skills': skills},
    )


class ProjectListView(generic.ListView):
    model = Project
    context_object_name = 'project_list'
    template_name = 'project_list.html'


class UserListView(generic.ListView):
    model = User
    context_object_name = 'user_list'
    template_name = 'user_list.html'


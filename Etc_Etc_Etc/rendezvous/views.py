from django.shortcuts import render
from .models import Skill, Tag, Event, Location, User, Project

def profile(request, id):
    """
    View function for the profile page.
    """
    user = User.objects.get(id=id)
    user_name = user.name
    user_skills = user.relevant_skills

    proj_created = user.projects_owned.order_by('-date_created')
    num_proj_created = proj_created.count()

    proj_contributed = user.projects_contributed.order_by('-date_joined')
    num_proj_contributed = proj_contributed.count()

    return render(
        request, 'profile.html',
        context={'user_name': user_name, 'user_skills': user_skills, 'proj_created': proj_created,
                 'num_proj_created': num_proj_created, 'num_proj_contributed': num_proj_contributed}
    )

def project(request, id):
    """
    View function for the project page.
    """
    project = Project.objects.get(id=id)
    proj_name = project.name
    proj_creator = project.owner
    proj_description = project.description
    proj_contributors = project.contributors
    skills_desired = project.skills_desired

    return render(
        request, 'project.html',
        context={'proj_name': proj_name, 'proj_creator': proj_creator, 'proj_description': proj_description,
                 'proj_contributors': proj_contributors, 'skills_desired': skills_desired}
    )
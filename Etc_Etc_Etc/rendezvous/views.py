from django.shortcuts import render
from .models import Skill, Tag, Event, Location, Profile, Project
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView
import datetime
from .forms import ProjectForm, ProfileForm, SearchForm
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.request import QueryDict


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


class ProjectListView(generic.ListView):
    """
    View function for project list view, generic view that is used for debug purposes.
    """
    model = Project
    context_object_name = 'project_list'
    template_name = 'project_list.html'


class ProfileListView(generic.ListView):
    """
    View function for the profile list view, generic view that is used for debug purposes.
    """
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
    """
    View for the project create page.
    """
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('view-project', args=(self.object.id.hex,))

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        form.instance.date_created = datetime.date.today()
        return super(ProjectCreate, self).form_valid(form)


class ProjectUpdate(UpdateView):
    """
    Generic view for the project update page.
    """
    model = Project
    form_class = ProjectForm


class ProfileUpdate(UpdateView):
    """
    Generic view for the profile update page.
    """
    model = Profile
    form_class = ProfileForm


def search_form_request(request):
    """
    View for the advanced search form page.
    """

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():

            skills = form.cleaned_data['skills_desired']
            if not skills.exists():
                skills = None
            location = form.cleaned_data['location']
            tags = form.cleaned_data['tags']
            if not tags.exists():
                tags = None
            all_name = form.cleaned_data['project_name']
            all_description = form.cleaned_data['description']

            qdict = QueryDict(mutable=True)
            if skills:
                qdict.setlist('skills', skills)
            if location:
                qdict['location'] = location
            if tags:
                qdict.setlist('tags', tags)
            if all_name:
                qdict['all_name'] = all_name
            if all_description:
                qdict['all_description'] = all_description

            return HttpResponseRedirect(reverse('search-results') + "?" + qdict.urlencode())
    else:
        form = SearchForm()

    return render(
        request,
        'search_form.html',
        {'form': form}
    )


def search_results(request):
    """
    View function for advanced search page.
    """

    skills = list()
    location = None
    tags = list()
    all_name = ""
    all_description = ""

    if 'skills' in request.GET:
        skills = request.GET.getlist('skills')
    if 'location' in request.GET:
        location = request.GET['location'].strip()
    if 'tags' in request.GET:
        tags = request.GET.getlist('tags')
    if 'all_name' in request.GET:
        all_name = request.GET['all_name'].strip()
    if 'all_description' in request.GET:
        all_description = request.GET['all_description'].strip()

    projects = Project.objects.all()

    # filter search terms here
    name_terms = all_name.split()
    desc_terms = all_description.split()

    name_land_include = list()  # list of terms in the name that must all appear
    desc_land_include = list()  # list of terms in the description that must all appear

    i = 0
    while i < len(name_terms):  # combines terms that are surrounded by quotes into one term
        if name_terms[i][0] == '"':
            for j in range(i + 1, len(name_terms)):
                if name_terms[j][-1:] == '"':
                    for part in range(i + 1, j + 1):
                        name_terms[i] += " " + name_terms[part]
                        name_terms.remove(name_terms[part])
                    name_terms[i] = name_terms[i][1:-1]
        i += 1
    i = 0
    while i < len(name_terms):  # makes a list of the terms that must all appear in the name
        if 0 < i < len(name_terms) and name_terms[i] == 'AND':
            name_land_include.append(name_terms[i - 1])
            name_land_include.append(name_terms[i + 1])
            for j in range(i + 1, i - 1, -1):
                name_terms.remove(name_terms[j])
                i -= 1
        i += 1

    i = 0
    while i < len(desc_terms):  # combines terms that are surrounded by quotes into one term
        if desc_terms[i][0] == '"':
            for j in range(i + 1, len(desc_terms)):
                if desc_terms[j][-1:] == '"':
                    for part in range(i + 1, j + 1):
                        desc_terms[i] += " " + desc_terms[part]
                        desc_terms.remove(desc_terms[part])
                    desc_terms[i] = desc_terms[i][1:-1]
        i += 1
    i = 0
    while i < len(desc_terms):  # makes a list of the terms that must all appear in the description
        print("Yes\n\n\n\n\n\n")
        if 0 < i < len(desc_terms) and desc_terms[i] == 'AND':
            desc_land_include.append(desc_terms[i - 1])
            desc_land_include.append(desc_terms[i + 1])
            for j in range(i + 1, i - 1, -1):
                desc_terms.remove(desc_terms[j])
                i -= 1
        i += 1

    # get Project objects and filter them now.
    temp_projects = projects
    if skills:
        for skill in skills:
            if temp_projects == projects:
                projects = projects.filter(skills_desired__name__icontains=skill)
            else:
                projects |= temp_projects.filter(skills_desired__name__icontains=skill)

    temp_projects = projects
    if tags:
        for tag in tags:
            if temp_projects == projects:
                projects = projects.filter(tags__tag__icontains=tag)
            else:
                projects |= temp_projects.filter(tags__tag__icontains=tag)

    if location:  # Out of all of the search implementation, this part is the very worst.
        loc_list = location.split(", ")
        if len(loc_list) > 0:
            projects = projects.filter(location__country=loc_list[0])
        if len(loc_list) > 1:
            projects = projects.filter(location__state=loc_list[1])
        if len(loc_list) > 2:
            projects = projects.filter(location__city=loc_list[2])
        if len(loc_list) > 3:
            projects = projects.filter(location__local_address=loc_list[3])

    for name_term in name_land_include:  # filters projects only to those that include required name terms
        projects = projects.filter(name__icontains=name_term)
    temp_projects = projects
    for name_term in name_terms:  # filters projects only to ones that include at least one of terms in name
        if temp_projects == projects:
            projects = projects.filter(name__icontains=name_term)
        else:
            projects |= temp_projects.filter(name__icontains=name_term)

    for desc_term in desc_land_include:  # filters projects to only those that include required desc terms
        projects = projects.filter(description__icontains=desc_term)
    temp_projects = projects
    for desc_term in desc_terms:  # filters projects to only those that include at least one of terms in desc
        if temp_projects == projects:
            projects = projects.filter(description__icontains=desc_term)
        else:
            projects |= temp_projects.filter(description__icontains=desc_term)

    projects = projects.distinct()
    projects = projects.order_by('name')

    page_object = Paginator(projects, 12)
    page = request.GET.get('page')
    try:
        projs = page_object.page(page)
    except PageNotAnInteger:
        projs = page_object.page(1)
    except EmptyPage:
        projs = page_object.page(page_object.num_pages)

    result_rows = list()
    for i in range(0, len(projs), 4):
        sublist = list()
        for j in range(4):
            if i + j < len(projs):
                sublist.append(projs[i+j])
            else:
                break
        result_rows.append(sublist)

    return render(
        request,
        'search_result.html',
        context={'result_rows': result_rows, 'project_page': projs},
    )

from django.db import models
from django.urls import reverse
import uuid


# Create your models here.
    
class Skill(models.Model):
    """
    Model representing a user's skill in a particular area(e.g. programming, dancing, baking, etc.).
    """
    name = models.CharField(max_length=50, help_text="Enter a unique skill (e.g. programming, dancing, etc.)")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
    
class Tag(models.Model):
    """
    Model representing a keyword/tag to make searching for relevant projects easier(e.g. programming, dancing, baking, etc.).
    """
    tag = models.CharField(max_length=50, help_text="Enter a unique tag/keyword (e.g. programming, dancing, etc.)")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.tag
    
class Event(models.Model):
    """
    Model representing a specific event associated with a user's project. (e.g. Performance, Presentation, etc.)"""
    
    name = models.CharField(max_length=50, help_text="Enter a name for the event.")
    description = models.CharField(max_length=500, help_text="Enter a brief description of the event.")
    date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Location(models.Model):
    """
    Model representing the location of a certain project/the area in which it is being conducted
    """
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    local_address = models.CharField(max_length=100)
    
    def __str__(self):
        return '%s, %s, %s' % (self.country, self.state, self.city)
    
    

class User(models.Model):
    """
    Model representing a specific user.
    """
    name = models.CharField(max_length=50)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="unique way to identify each user.")
    email = models.CharField(max_length=50)
    relevant_skills = models.ManyToManyField(Skill, help_text="Select one of your relevant skills.")
    # ManyToManyField used because skill can contain many users. Users can cover many skills.
    # Skill class has already been defined so we can specify the object above.
    projects_owned = models.ManyToManyField(Project, blank = True, help_text="Select a project that this user owns.")
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular user.
        """
        return reverse('user', args=[str(self.id)])
    
class Project(models.Model):
    """
    Model representing a specific project.
    """
    name = models.CharField(max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="unique way to identify each project.")
    owner = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=500)
    tags = models.ManyToManyField(Tag, help_text="Select relevant tags so users can find your project.")
    skills_desired = models.ManyToManyField(Skill, help_text="Select one of the relevant skills that you are looking for.")
    # ManyToManyField used because skill can contain many projects. Projects can cover many skills.
    # Skill class has already been defined so we can specify the object above.
    events = models.ManyToManyField(Event)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)
    contributors = models.ManyToManyField(User, blank=True, help_text="User that is contributing to this project.")
    date_created = models.DateField(null=True, blank=True)
    date_completed = models.DateField(null=True, blank=True)
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular project.
        """
        return reverse('project', args=[str(self.id)])

from django.db import models

# Create your models here.
# Project & TCCS
class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    executive_summary = models.TextField()
    schedule = models.DateTimeField()
    objective = models.TextField()  
    methodology = models.TextField()
    current_status = models.TextField()
    percent_complete = models.IntegerField()
    additional_information = models.TextField()

class Collaborator(models.Model):
    collab_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='collaborators')
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)

class Funding(models.Model):
    funding_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='fundings')
    sponsor = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='resources')
    resource_type = models.CharField(max_length=255)
    description = models.TextField()

class Commercialization(models.Model):
    commercialization_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='commercializations')
    industrial_benefits = models.TextField()
    rnd_benefits = models.TextField()
    contribution_nca = models.TextField()

class NewInvention(models.Model):
    invention_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='new_inventions')
    name = models.CharField(max_length=255)
    description = models.TextField()
    applications = models.TextField()

class OngoingProject(models.Model):
    related_project_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ongoing_projects')
    title = models.CharField(max_length=255)
    description = models.TextField()

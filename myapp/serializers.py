from rest_framework import serializers
from .models import Project, Collaborator, Funding, Resource, Commercialization, NewInvention, OngoingProject
import logging

logger = logging.getLogger(__name__)

class CollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaborator
        fields = ['name', 'role']

class FundingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funding
        fields = ['sponsor', 'amount']

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['resource_type', 'description']

class CommercializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commercialization
        fields = ['industrial_benefits', 'rnd_benefits', 'contribution_nca']

class NewInventionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewInvention
        fields = ['name', 'description', 'applications']

class OngoingProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = OngoingProject
        fields = ['title', 'description']

class ProjectSerializer(serializers.ModelSerializer):
    collaborators = CollaboratorSerializer(many=True)
    fundings = FundingSerializer(many=True)
    resources = ResourceSerializer(many=True)
    commercializations = CommercializationSerializer(many=True)
    new_inventions = NewInventionSerializer(many=True)
    ongoing_projects = OngoingProjectSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            'title', 'executive_summary', 'schedule', 'objective',
            'methodology', 'current_status', 'percent_complete',
            'additional_information', 'collaborators', 'fundings',
            'resources', 'commercializations', 'new_inventions',
            'ongoing_projects'
        ]

    def create(self, validated_data):
        # Extract nested data
        collaborators_data = validated_data.pop('collaborators', [])
        fundings_data = validated_data.pop('fundings', [])
        resources_data = validated_data.pop('resources', [])
        commercializations_data = validated_data.pop('commercializations', [])
        new_inventions_data = validated_data.pop('new_inventions', [])
        ongoing_projects_data = validated_data.pop('ongoing_projects', [])
        
        # Create the main Project instance
        project = Project.objects.create(**validated_data)

        # Create related objects
        self._create_related_objects(Collaborator, collaborators_data, project, 'project')
        self._create_related_objects(Funding, fundings_data, project, 'project')
        self._create_related_objects(Resource, resources_data, project, 'project')
        self._create_related_objects(Commercialization, commercializations_data, project, 'project')
        self._create_related_objects(NewInvention, new_inventions_data, project, 'project')
        self._create_related_objects(OngoingProject, ongoing_projects_data, project, 'project')

        return project

    def _create_related_objects(self, model, data_list, project, project_field_name):
        """
        Utility method to create related objects for a project.
        """
        for data in data_list:
            try:
                model.objects.create(**{project_field_name: project}, **data)
                logger.info(f"{model.__name__} created with data: {data}")
            except Exception as e:
                logger.error(f"Error creating {model.__name__}: {e}")

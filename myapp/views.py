from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProjectSerializer
import logging

logger = logging.getLogger(__name__)

class ProjectCreateView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info("POST request received at ProjectCreateView")
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            logger.info("Serializer is valid")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
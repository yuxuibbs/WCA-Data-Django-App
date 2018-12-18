from wca.models import Result
from wca.models import Person
from api.serializers import ResultSerializer
from api.serializers import PersonSerializer
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.select_related('person').order_by('competition', 'event')
    serializer_class =  ResultSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def delete(self, request, pk, format=None):
        result = self.get_object(pk)
        self.perform_destroy(self, result)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class =  PersonSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def delete(self, request, pk, format=None):
        person = self.get_object(pk)
        self.perform_destroy(self, person)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


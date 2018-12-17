from wca.models import Result
from api.serializers import ResultSerializer
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.select_related('person_identifier').order_by('competition_identifier', 'event_identifier', 'round_type_identifier')
    serializer_class =  ResultSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def delete(self, request, pk, format=None):
        result = self.get_object(pk)
        self.perform_destroy(self, result)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()



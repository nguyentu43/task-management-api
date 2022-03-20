from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView


class ModelViewSetWithPermission(ModelViewSet):

    permission_classes_by_action = {}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

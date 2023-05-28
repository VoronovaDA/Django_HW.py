from django.db.models import Q
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.exceptions import PermissionDenied

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from .filters import AdvertisementFilter
from .models import Advertisement, FavoriteAdvertisement
from .permissions import IsOwnerOrAdminOrReadOnly
from .serializers import AdvertisementSerializer, FavoriteAdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    def list(self, request, *args, **kwargs):

        if request.user.is_superuser:
            queryset = self.filter_queryset(self.get_queryset()) # self.get_queryset()=Advertisement.objects.all()
        elif request.user.is_authenticated:
            queryset = self.filter_queryset(self.get_queryset().filter(Q(status='DRAFT', creator_id=request.user.id) | Q(status__in=['OPEN', 'CLOSED'])))
        else:
            queryset = self.filter_queryset(self.get_queryset().exclude(status='DRAFT'))
        serializer = AdvertisementSerializer(queryset, many=True)

        return Response(serializer.data)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ['favorites']:
            return [IsAuthenticated()]
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrAdminOrReadOnly()]
        return []

    @action(methods=['POST', 'GET'], detail=False)
    def favorites(self, request):
        user = request.user.id

        if request.method == 'GET':
            id_adv = [i[2] for i in FavoriteAdvertisement.objects.filter(user_id=user).values_list()]
            queryset = Advertisement.objects.filter(id__in=id_adv)
            serializer = AdvertisementSerializer(queryset, many=True)

            return Response(serializer.data)

        else:
            request.data["user"] = user
            serializer = FavoriteAdvertisementSerializer(data=request.data)

            if serializer.is_valid():
                adv_owner = Advertisement.objects.filter(id=request.data['advertisement'])[0].creator_id
                if user != adv_owner:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response({'error': 'you can add your own adv to favorites'}, status=status.HTTP_403_FORBIDDEN)

            return Response({'message': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

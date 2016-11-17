from django.core import exceptions as django_exceptions
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework import generics, permissions, response, status, views
from .models import Author
from .serializers import AuthorSerializer, FullAuthorSerializer, AuthenticateSerializer, \
    UpdateAuthorSerializer, AuthorNetworkSerializer
from . import permissions as my_permissions


class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class AuthorCreateView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = FullAuthorSerializer
    permission_classes = [permissions.AllowAny]


class AuthorUpdateView(generics.UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = UpdateAuthorSerializer
    permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerForModifyAuthor]


class AuthorRetrieveView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = FullAuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthorAuthenticationView(views.APIView):
    queryset = Author.objects.all()
    serializer_class = AuthenticateSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = AuthenticateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return response.Response(new_data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorNetworkView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorNetworkSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthorFollowView(viewsets.ModelViewSet):
    serializer_class = AuthorNetworkSerializer
    permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerForAccessAuthor]

    def get_queryset(self):
        result_list = Author.objects.filter(id=self.request.user.author.id)
        return result_list

    @detail_route(methods=['put'])
    def follow(self, request, **kwargs):
        author = request.user.author
        try:
            to_be_followed = Author.objects.get(id=kwargs['pk'])
        except django_exceptions.ObjectDoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        author.following.add(to_be_followed)
        to_be_followed.followers.add(author)
        return response.Response(status=status.HTTP_202_ACCEPTED)


class AuthorUnfollowView(viewsets.ModelViewSet):
    serializer_class = AuthorNetworkSerializer
    permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerForAccessAuthor]

    def get_queryset(self):
        result_list = Author.objects.filter(id=self.request.user.author.id)
        return result_list

    @detail_route(methods=['put'])
    def unfollow(self, request, **kwargs):
        author = request.user.author
        try:
            to_be_unfollowed = Author.objects.get(id=kwargs['pk'])
        except django_exceptions.ObjectDoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        author.following.remove(to_be_unfollowed)
        to_be_unfollowed.followers.remove(author)
        return response.Response(status=status.HTTP_202_ACCEPTED)

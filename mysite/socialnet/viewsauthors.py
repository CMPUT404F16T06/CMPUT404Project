from itertools import chain
import requests
from django.contrib.auth.models import User
from django.core import exceptions as django_exceptions
from django.shortcuts import get_object_or_404
from requests.auth import HTTPBasicAuth
from rest_framework import generics, permissions, response, status, views
from rest_framework import viewsets
from rest_framework.decorators import detail_route
import uuid

from . import permissions as my_permissions
from .models import Author, FriendRequest, Node
from .serializers import FullAuthorSerializer, AuthenticateSerializer, \
	UpdateAuthorSerializer, AuthorNetworkSerializer, AuthorFriendSerializer, \
	FriendRequestSerializer, RemoteRequestSerializer


class AuthorListView(generics.ListAPIView):
	queryset = Author.objects.all()
	serializer_class = AuthorFriendSerializer


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
	serializer_class = AuthorFriendSerializer
	permission_classes = [permissions.IsAuthenticated]


class AuthorAuthenticationView(views.APIView):
	queryset = Author.objects.all()
	serializer_class = AuthenticateSerializer

	def post(self, request):
		data = request.data
		serializer = AuthenticateSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data = serializer.data
			return response.Response(new_data, status=status.HTTP_200_OK)
		return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorNetworkView(generics.RetrieveAPIView):
	queryset = Author.objects.all()
	serializer_class = AuthorNetworkSerializer


class SendFriendRequestView(viewsets.ModelViewSet):
	serializer_class = AuthorNetworkSerializer

	def get_author_info(self, request, key_name):
		res = dict()
		node = request.data[key_name]["host"]
		return node

	def get_queryset(self):
		result_list = FriendRequest.objects.filter(receiver=self.request.user.author)
		return result_list

	@detail_route(methods=['post'])
	def send_request(self, request, **kwargs):
		try :
			author = request.user.author
			receiver = get_object_or_404(Author, id=kwargs['pk'])
			try:
				FriendRequest.objects.get(sender=author, receiver=author)
				return response.Response(status=status.HTTP_400_BAD_REQUEST)
			except django_exceptions.ObjectDoesNotExist:
				pass
			friendRequest = FriendRequest.objects.create(sender=author, receiver=receiver)
			friendRequest.save()
			return response.Response(status=status.HTTP_202_ACCEPTED)
		except AttributeError:
			return response.Response(status=status.HTTP_400_BAD_REQUEST)


class SendRemoteFriendRequestView(viewsets.ModelViewSet):
	serializer_class = RemoteRequestSerializer
	queryset = FriendRequest.objects.all()

	def send_to_remote(self, url, data):
		r = requests.post(url, json=data, auth=("haha", "haha"))
		return r

	def makeAuthor(self, data, node_url):
		id = data['id']
		username = data['displayname'].split(" ")[0]
		first_name = username
		last_name = username
		email = username + "@nousageemail.com"
		try:
			user = User.objects.create(username=username,
			                           first_name=first_name, last_name=last_name, email=email)
		except:
			return User.objects.get(username=username)
		author = Author.objects.create(user=user, id=uuid.UUID(id),
		                               displayname=str(data['displayname']), github="noGitHUB",
		                               host=node_url, url=node_url+"/author/"+id)
		return author

	@detail_route(methods=['post'])
	def send_request(self, request):
		try:
			print request.data['author.host']
			print request.data['friend.host']
			node_author = Node.objects.get(node_url=str(request.data['author.host']))
			node_friend = Node.objects.get(node_url=str(request.data['friend.host']))
		except django_exceptions.ObjectDoesNotExist:
			return response.Response(status=status.HTTP_403_FORBIDDEN)
		serializer = RemoteRequestSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			data = serializer.data
			try:
				author = Author.objects.get(id=request.data['author.id'])
			except django_exceptions.ObjectDoesNotExist:
				author = self.makeAuthor(data['author'], node_author.node_url)
			try:
				friend = Author.objects.get(id=request.data['friend.id'])
			except django_exceptions.ObjectDoesNotExist:
				friend = self.makeAuthor(data['friend'], node_friend.node_url)
			print str(author.id) + "\n\n\n"
			print str(friend.id) + "\n\n\n"
			try:
				friendRequest = FriendRequest.objects.create(sender=friend, receiver=author)
			except:
				pass
			#res = self.send_to_remote(node_author.node_url+'friendrequest/', request.data)
			#print str(res)
			#return response.Response(status=status.HTTP_200_OK)


class FriendRequestByAuthorView(generics.ListAPIView):
	serializer_class = FriendRequestSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		result_list = FriendRequest.objects.filter(receiver=self.request.user.author)
		result_list = list(chain(result_list, FriendRequest.objects.filter(sender=self.request.user.author)))
		return result_list


class AcceptFriendRequestView(viewsets.ModelViewSet):
	serializer_class = AuthorNetworkSerializer
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerForAccessAuthor]

	def get_queryset(self):
		result_list = FriendRequest.objects.filter(receiver=self.request.user.author)
		return result_list

	@detail_route(methods=['post'])
	def accept_request(self, request, **kwargs):
		receiver = request.user.author
		sender = get_object_or_404(Author, id=kwargs['pk'])
		friend_req = get_object_or_404(FriendRequest, sender=sender)
		friend_req.delete()
		receiver.friends.add(sender)
		return response.Response(status=status.HTTP_202_ACCEPTED)

	@detail_route(methods=['delete'])
	def reject_request(self, request, **kwargs):
		receiver = request.user.author
		sender = get_object_or_404(Author, id=kwargs['pk'])
		friend_req = get_object_or_404(FriendRequest, sender=sender)
		friend_req.delete()
		return response.Response(status=status.HTTP_202_ACCEPTED)


class UnfriendView(viewsets.ModelViewSet):
	serializer_class = AuthorNetworkSerializer
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerForAccessAuthor]

	def get_queryset(self):
		result_list = FriendRequest.objects.filter(receiver=self.request.user.author)
		return result_list

	@detail_route(methods=['delete'])
	def unfriend(self, request, **kwargs):
		unfriender = request.user.author
		unfriended = get_object_or_404(Author, id=kwargs['pk'])
		unfriender.friends.remove(unfriended)
		return response.Response(status=status.HTTP_202_ACCEPTED)



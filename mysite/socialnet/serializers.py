from django.db.models import Q
from rest_framework import serializers
from rest_framework import exceptions
from rest_framework.exceptions import ValidationError

from .models import Post, Author
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
	first_name = serializers.CharField(source='author.user.first_name')
	last_name = serializers.CharField(source='author.user.last_name')

	class Meta:
		model = Post
		fields = [
			'id',
			'published_date',
			'author',
			'text',
			'public',
			'first_name',
			'last_name',
		]


class CreatePostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = [
			'id',
			'published_date',
			'text',
			'public',
		]


class FriendDataSerializer(serializers.ModelSerializer):
	first_name = serializers.CharField(source='user.first_name')
	last_name = serializers.CharField(source='user.last_name')

	class Meta:
		model = Author
		fields = [
			'id',
			'first_name',
			'last_name',
			'avatar',
		]


class AuthorSerializer(serializers.ModelSerializer):
	first_name = serializers.CharField(source='user.first_name')
	last_name = serializers.CharField(source='user.last_name')
	email = serializers.CharField(source='user.email')
	friends = FriendDataSerializer(many=True)

	class Meta:
		model = Author
		fields = [
			'id',
			'first_name',
			'last_name',
			'github',
			'avatar',
			'friends',
			'email',
		]


class FriendsAuthorSerializer(serializers.ModelSerializer):
	friends = FriendDataSerializer(many=True)

	class Meta:
		model = Author
		fields = [
			'friends',
		]


class FriendRequestsAuthorSerializer(serializers.ModelSerializer):
	friend_requests = FriendDataSerializer(many=True)

	class Meta:
		model = Author
		fields = [
			'friend_requests',
		]


class FullAuthorSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source='user.username')
	email = serializers.CharField(source='user.email')
	first_name = serializers.CharField(source='user.first_name')
	last_name = serializers.CharField(source='user.last_name')
	password = serializers.CharField(source='user.password', style={'input_type': 'password'})

	class Meta:
		model = Author
		fields = [
			'id',
			'username',
			'password',
			'email',
			'first_name',
			'last_name',
			'github',
			'avatar',
			'date_created',
		]

	# extra_kwargs = {"password" : {"write_only": True}}

	# http://stackoverflow.com/questions/29457630/extend-user-model-django-rest-framework-3-x-x

	def update(self, instance, validated_data):
		user_data = validated_data.pop('user', None)
		for attr, value in user_data.items():
			setattr(instance.user, attr, value)
		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		instance.save()
		return instance

	def create(self, validated_data):
		user_data = validated_data.pop('user')
		user = User.objects.create(**user_data)
		user.set_password(user_data['password'])
		user.save()
		author = Author.objects.create(user=user, **validated_data)
		return author


class AuthenticateSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source='user.username')
	password = serializers.CharField(source='user.password', style={'input_type': 'password'})
	author = AuthorSerializer(allow_null=True, read_only=True)
	class Meta:
		model = User
		depth = 1
		fields = [
			'username',
			'password',
			'author',
		]
		extra_kwargs = {"password": {"write_only": True}}

	def validate(self, attrs):
		validation_data = dict(attrs)['user']
		username = validation_data.get('username', None);
		password = validation_data.get('password', None);
		try:
			user = User.objects.get(username=username)
		except:
			raise ValidationError("Incorrect login/password.")
		if user.check_password(password):
			attrs['author'] = user.author
			return attrs
		raise ValidationError("Incorrect login/password.")
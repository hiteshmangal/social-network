from rest_framework import serializers
from .models import FriendRequest

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status']
        read_only_fields = ['from_user', 'status']


class UpdateFriendRequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['status']
        read_only_fields = ['from_user', 'to_user', 'id']
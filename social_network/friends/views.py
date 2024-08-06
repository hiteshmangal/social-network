from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FriendRequest 
from users.models import User
from django.db.models import Q
from .serializers import FriendRequestSerializer , UpdateFriendRequestStatusSerializer
from users.serializers import UserSerializer
from rest_framework.throttling import UserRateThrottle
from rest_framework.pagination import PageNumberPagination

from rest_framework.throttling import UserRateThrottle

class FriendRequestThrottle(UserRateThrottle):
    scope = 'friend_request'


    
class SendFriendRequestView(generics.CreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user, status='sent')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        recipient_id = request.data.get('to_user')
        recipient = User.objects.filter(id=recipient_id).first()
        
        if recipient:
            response_data = {
                'message': 'Friend request sent successfully.',
                'recipient': {
                    'id': recipient.id,
                    'name': recipient.get_full_name() 
                }
            }
        else:
            response_data = {
                'message': 'Friend request sent, but recipient not found.',
            }
        
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


    
class AcceptFriendRequestView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = UpdateFriendRequestStatusSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            friend_request = FriendRequest.objects.get(pk=pk)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)

        if friend_request.to_user != request.user:
            return Response({'error': 'You are not authorized to accept this friend request.'}, status=status.HTTP_403_FORBIDDEN)

        friend_request.status = 'accepted'
        friend_request.save()

       
        sender = friend_request.from_user

        response_data = {
            'status': 'Friend request accepted.',
            'sender': {
                'id': sender.id,
                'name': sender.get_full_name(), 
                'email': sender.email
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

    
class RejectFriendRequestView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = UpdateFriendRequestStatusSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            friend_request = FriendRequest.objects.get(pk=pk)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)

        if friend_request.to_user != request.user:
            return Response({'error': 'You are not authorized to reject this friend request.'}, status=status.HTTP_403_FORBIDDEN)

        friend_request.status = 'rejected'
        friend_request.save()

        sender = friend_request.from_user

        response_data = {
            'status': 'Friend request rejected.',
            'sender': {
                'id': sender.id,
                'name': sender.get_full_name(),  
                'email': sender.email
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)


    
class ListFriendsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        friends = FriendRequest.objects.filter(
            Q(from_user=user, status='accepted') |
            Q(to_user=user, status='accepted')
        )
        friend_ids = [f.from_user.id if f.to_user == user else f.to_user.id for f in friends]
        return User.objects.filter(id__in=friend_ids)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            total_friends = queryset.count()
        else:
            serializer = self.get_serializer(queryset, many=True)
            total_friends = queryset.count()

        pending_requests = FriendRequest.objects.filter(to_user=self.request.user, status='pending').count()

        return Response({
            'friends': serializer.data,
            'total_friends': total_friends,
            'pending_requests': pending_requests
        }, status=status.HTTP_200_OK)

class ListPendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user, status='sent')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            pending_requests_count = queryset.count()
        else:
            serializer = self.get_serializer(queryset, many=True)
            pending_requests_count = queryset.count()

        return Response({
            'pending_requests': serializer.data,
            'pending_requests_count': pending_requests_count
        }, status=status.HTTP_200_OK)
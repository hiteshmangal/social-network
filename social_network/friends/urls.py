from django.urls import path
from .views import SendFriendRequestView, AcceptFriendRequestView, RejectFriendRequestView, ListFriendsView, ListPendingRequestsView

urlpatterns = [
    path('send-request/', SendFriendRequestView.as_view(), name='send-request'),
    path('accept-request/<int:pk>/', AcceptFriendRequestView.as_view(), name='accept-request'),
    path('reject-request/<int:pk>/', RejectFriendRequestView.as_view(), name='reject-request'),
    path('friends/', ListFriendsView.as_view(), name='list-friends'),
    path('pending-requests/', ListPendingRequestsView.as_view(), name='list-pending-requests'),
]
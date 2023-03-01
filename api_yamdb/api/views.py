from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import ScopedRateThrottle
from reviews.models import Comment, Review, Title

from .permissions import IsOwnerOrModeratorOrAdmin
from .rating import update_rating
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    throttle_classes = (ScopedRateThrottle,)
    pagination_class = PageNumberPagination
    permission_classes = (IsOwnerOrModeratorOrAdmin,)

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        user = self.request.user
        serializer.save(
            author=user, title=title)
        update_rating(title_id)

    def perform_update(self, serializer):
        title_id = self.kwargs.get("title_id")
        super(ReviewViewSet, self).perform_update(serializer)
        update_rating(title_id)

    def perform_destroy(self, serializer):
        title_id = self.kwargs.get("title_id")
        super(ReviewViewSet, self).perform_destroy(serializer)
        update_rating(title_id)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    throttle_classes = (ScopedRateThrottle,)
    pagination_class = PageNumberPagination
    permission_classes = (IsOwnerOrModeratorOrAdmin,)

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        user = self.request.user
        serializer.save(
            author=user, review=review)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        new_queryset = Comment.objects.filter(review=review_id)
        return new_queryset

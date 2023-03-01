from django.db.models import Avg
from django.shortcuts import get_object_or_404
from reviews.models import Review, Title


def update_rating(title_id):
    title = get_object_or_404(Title, id=title_id)
    reviews = Review.objects.filter(title=title_id)
    rating_value = None
    if reviews:
        average_score = reviews.aggregate(Avg('score'))
        print(average_score)
        print(round(average_score['score__avg'], 0))
        rating_value = int(round(average_score['score__avg'], 0))

    print(rating_value)
    title.rating = rating_value
    title.save()
    return rating_value

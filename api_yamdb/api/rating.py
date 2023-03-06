from django.db.models import Avg
from reviews.models import Title


def update_rating(title):
    rating_value = None
    t = Title.objects.filter(
        id=title.id).annotate(avg_rating=Avg('reviews__score'))
    if t[0].avg_rating:
        rating_value = int(round(t[0].avg_rating, 0))
    print(rating_value)
    title.rating = rating_value
    title.save()
    return title

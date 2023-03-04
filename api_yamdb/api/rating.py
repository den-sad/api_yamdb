from django.db.models import Avg


def update_rating(title):
    rating_value = None
    average_score = title.reviews.aggregate(Avg('score'))
    if average_score['score__avg']:
        rating_value = int(round(average_score['score__avg'], 0))
    title.rating = rating_value
    title.save()
    return title

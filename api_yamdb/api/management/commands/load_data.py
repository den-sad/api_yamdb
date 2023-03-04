from csv import DictReader

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User

ALREDY_LOADED_ERROR_MESSAGE = """
Если надо перезалить данные из CSV файла,
то сначала надо удалить файл базы db.sqlite3.
Затем запустить `python manage.py migrate` для
новой пустой базы с таблицами.
"""

models = [Category, Genre, Comment, Review, Title, User]


class Command(BaseCommand):
    help = "Загружает данные из category.csv"

    def handle(self, *args, **options):
        # Проверка на то, что в базе еще нет данных
        for model in models:
            if model.objects.exists():
                print(f'Данные в таблицу {model} уже загружены.')
                print(ALREDY_LOADED_ERROR_MESSAGE)
                return

        print("Загрузка данных")
        # Код загрузки
        for row in DictReader(open('./static/data/users.csv')):
            table = User(
                id=row['id'], username=row['username'], email=row['email'],
                bio=row['bio'], role=row['role'], first_name=row['first_name'],
                last_name=row['last_name']
            )
            table.save()

        for row in DictReader(open('./static/data/category.csv')):
            table = Category(id=row['id'], name=row['name'], slug=row['slug'])
            table.save()

        for row in DictReader(open('./static/data/genre.csv')):
            table = Genre(id=row['id'], name=row['name'], slug=row['slug'])
            table.save()

        for row in DictReader(open('./static/data/titles.csv')):
            table = Title(
                id=row['id'], name=row['name'], year=row['year'],
                category_id=int(row['category'])
            )
            table.save()

        for row in DictReader(open('./static/data/review.csv')):
            table = Review(
                id=row['id'], text=row['text'], author_id=row['author'],
                score=row['score'], title_id=row['title_id'],
                pub_date=row['pub_date']
            )
            table.save()

        for row in DictReader(open('./static/data/comments.csv')):
            table = Comment(
                id=row['id'], review_id=row['review_id'], text=row['text'],
                author_id=row['author'], pub_date=row['pub_date']
            )
            table.save()

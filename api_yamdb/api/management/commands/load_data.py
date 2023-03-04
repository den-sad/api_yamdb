from csv import DictReader

from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    help = "Загружает данные из файлов csv"

    def users_loader(self):
        with open("static/data/users.csv", newline='') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                try:
                    User.objects.update_or_create(
                        id=row['id'], username=row['username'],
                        email=row['email'], bio=row['bio'], role=row['role'],
                        first_name=row['first_name'],
                        last_name=row['last_name']
                    )
                except Exception as error:
                    raise CommandError(
                        f'Ошибка записи в таблице модели User, {str(error)}'
                    )

    def category_loader(self):
        with open("static/data/category.csv", newline='') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                try:
                    Category.objects.update_or_create(
                        id=row['id'], name=row['name'], slug=row['slug']
                    )
                except Exception as error:
                    raise CommandError(
                        f'Ошибка записи в таблице модели Category, '
                        f'{str(error)}, в строке {row}'
                    )

    def genre_loader(self):
        with open("static/data/genre.csv", newline='') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                try:
                    Genre.objects.update_or_create(
                        id=row['id'], name=row['name'], slug=row['slug']
                    )
                except Exception as error:
                    raise CommandError(
                        f'Ошибка записи в таблице модели Genre, {str(error)}'
                    )

    def title_loader(self):
        with open("static/data/titles.csv", newline='') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                try:
                    Title.objects.update_or_create(
                        id=row['id'], name=row['name'], year=row['year'],
                        category_id=int(row['category'])
                    )
                except Exception as error:
                    raise CommandError(
                        f'Ошибка записи в таблице модели Title, {str(error)}'
                    )

    def review_loader(self):
        with open("static/data/review.csv", newline='') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                try:
                    Review.objects.update_or_create(
                        id=row['id'], text=row['text'],
                        author_id=row['author'], score=row['score'],
                        title_id=row['title_id'], pub_date=row['pub_date']
                    )
                except Exception as error:
                    raise CommandError(
                        f'Ошибка записи в таблице модели Review, {str(error)}'
                    )

    def comments_loader(self):
        with open("static/data/comments.csv", newline='') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                try:
                    Comment.objects.update_or_create(
                        id=row['id'], review_id=row['review_id'],
                        text=row['text'], author_id=row['author'],
                        pub_date=row['pub_date']
                    )
                except Exception as error:
                    raise CommandError(
                        f'Ошибка записи в таблице модели Comment, {str(error)}'
                    )

    def handle(self, *args, **options):

        print("Идет загрузка данных")

        print("Загружаем данные пользователей")
        self.users_loader()

        print("Загружаем категории")
        self.category_loader()

        print("Загружаем жанры")
        self.genre_loader()

        print("Загружаем произведения")
        self.title_loader()

        print("Загружаем ревью")
        self.review_loader()

        print("Загружаем комментарии")
        self.comments_loader()

        print('Загрука завершена.')

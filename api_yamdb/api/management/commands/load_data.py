from csv import DictReader

from django.conf import settings as conf_settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User

data_dir = conf_settings.STATICFILES_DIRS

csv_files = [
    {'model': User, 'filename': 'users.csv',
     'fieldnames': ['id', 'username', 'email', 'role',
                    'bio', 'first_name', 'last_name']},
    {'model': Category, 'filename': 'category.csv',
     'fieldnames': ['id', 'name', 'slug']},
    {'model': Genre, 'filename': 'genre.csv',
     'fieldnames': ['id', 'name', 'slug']},
    {'model': Title, 'filename': 'titles.csv',
     'fieldnames': ['id', 'name', 'year', 'category_id']},
    {'model': Review, 'filename': 'review.csv',
     'fieldnames': ['id', 'title_id', 'text',
                    'author_id', 'score', 'pub_date']},
    {'model': Comment, 'filename': 'comments.csv',
     'fieldnames': ['id', 'review_id', 'text', 'author_id', 'pub_date']},
]


class Command(BaseCommand):
    help = "Загружает данные из файлов csv"

    def csv_loader(self, cf):
        csv_file = '{}\\data\\{}'.format(data_dir[0], cf['filename'])
        with open(csv_file, encoding='utf-8', newline='') as csvfile:
            reader = DictReader(csvfile, fieldnames=cf['fieldnames'])
            print(f'Загрузка в таблицу модели {cf["model"].__name__}')

            i, err, r = 0, 0, 0

            for row in reader:
                if i != 0:
                    try:
                        id = row.pop('id')
                        cf['model'].objects.update_or_create(
                            id=id, defaults=row)
                        r += 1
                    except Exception as error:
                        print(row)
                        print(
                            f'Ошибка записи в таблицу модели '
                            f'{cf["model"].__name__}, '
                            f'{str(error)}')
                        err += 1
                i += 1
            print(
                f'Всего: {i-1} строк. Загружено: {r} строк. '
                f'Ошибки: {err} строк.')

    def handle(self, *args, **options):
        print("Идет загрузка данных")
        for сf in csv_files:
            self.csv_loader(сf)
        print('Загрука завершена.')

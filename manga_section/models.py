from django.db import models


class Genre(models.Model):
    genre_name = models.CharField(max_length=25,
                                  unique=True,
                                  verbose_name="Жанр")

    def __str__(self):
        return self.genre_name


class Author(models.Model):
    author_name = models.CharField(max_length=50,
                                   unique=True,
                                   verbose_name='Автор')

    def __str__(self):
        return self.author_name

class Staff(models.Model):
    staff_name = models.CharField(max_length=50,)
    link_for_offers = models.URLField(max_length=250,
                                      verbose_name='Ссылка для связи')

    def __str__(self):
        return self.staff_name
    

class Manga(models.Model):
    manga_name = models.CharField(max_length=150,
                                  verbose_name='Название')
    manga_slug = models.SlugField(max_length=200,
                                  verbose_name='SLUG-адрес',
                                  unique=True)
    genres = models.ManyToManyField(Genre,
                                    verbose_name='Жанр')
    authors = models.ManyToManyField(Author,
                                     verbose_name='Автор')
    description = models.TextField(verbose_name='Описание')

    def get_latest_volume_cover(self):
        # Получаем последний том по номеру (или по дате, если нужно)
        latest_volume = self.volumes.order_by('-vol_number').first()
        if latest_volume and latest_volume.vol_cover:
            return latest_volume.vol_cover
        return None

    def __str__(self):
        return self.manga_name

def volume_cover_path(instance, filename):
    return f'manga/volumes/covers/{instance.id}/{filename}'

class Volume(models.Model):
    manga = models.ForeignKey(Manga,
                              on_delete=models.CASCADE,
                              related_name='volumes',
                              verbose_name='Манга')
    vol_number = models.PositiveIntegerField(verbose_name='Номер тома')
    vol_cover = models.ImageField(upload_to=volume_cover_path)

    def __str__(self):
        return f'Том {str(self.vol_number)}'


class Chapter(models.Model):
    volume = models.ForeignKey(Volume,
                              on_delete=models.CASCADE,
                              related_name='chapters',
                              verbose_name='Манга')
    ch_number = models.FloatField(verbose_name='Номер')
    ch_name = models.CharField(max_length=100,
                               verbose_name='Название')
    add_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата и время создания')
    interpreter = models.ManyToManyField(Staff,
                                         verbose_name='Переводчик',
                                         related_name='interpreters',
                                         blank=True,
                                         default=None)
    editor = models.ManyToManyField(Staff,
                                    verbose_name='Редактор',
                                    related_name='editors',
                                    blank=True,
                                    default=None)
    retoucher = models.ManyToManyField(Staff,
                                       verbose_name='Ретушёр',
                                       related_name='retouchers',
                                       blank=True,
                                       default=None)
    typesetter = models.ManyToManyField(Staff,
                                        verbose_name='Верстальщик',
                                        related_name='typesetters',
                                        blank=True,
                                        default=None)
    sfx_artist = models.ManyToManyField(Staff,
                                        verbose_name='Художник по звукам',
                                        related_name='sfx_artists',
                                        blank=True,
                                        default=None)

    def __str__(self):
        return f'Глава {str(self.ch_number)}'

    def get_chapter_display(self):
        num = float(self.ch_number)
        if num.is_integer():
            return str(int(num))
        else:
            return str(num)

    def count_likes(self):
        return self.likes.filter(is_like=True).count()

    def count_all_rates(self):
        return self.likes.count()

    def rate_percentage(self):
        if self.count_all_rates() > 0:
            return round((self.count_likes() / self.count_all_rates()) * 100)
        else:
            return 0

    def get_next_chapter(self):
        try:
            return Chapter.objects.filter(
                volume__manga=self.volume.manga,
                ch_number__gt=self.ch_number
            ).order_by('ch_number').first()
        except:
            return None

def chapter_image_path(instance, filename):
    return f'manga/chapters/images/{instance.chapter.id}/{filename}'


class ChapterImage(models.Model):
    chapter = models.ForeignKey(Chapter,
                                on_delete=models.CASCADE,
                                related_name='images')
    page_number = models.PositiveIntegerField(verbose_name='Номер страницы')
    page_image = models.ImageField(upload_to=chapter_image_path,  # Используем функцию
                                   verbose_name='Страница')
    is_double_page = models.BooleanField(default=False)

    def __str__(self):
        return f"Страница {self.page_number}"

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from datetime import datetime
from os import path


def image_file_path(_instance, filename):
    ext = path.splitext(filename)[1]
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return f'images/image_{timestamp}{ext}'


def model_file_path(instance, _filename):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return f'models_3d/model_{instance.version}_{timestamp}.glb'


class FlightLocation(models.Model):
    FLIGHT_TYPE_CHOICES = [
        ('static_frame', 'Статичний кадр'),
        ('points_flight', 'Обліт по точках'),
        ('panorama', 'Панорама навколо'),
    ]

    CAMERA_VIEW_DIRECTION_CHOICES = [
        ('inside', 'Дивитися всередину'),
        ('outside', 'Дивитися назовні'),
        ('direction', 'Дивитися за напрямком руху'),
    ]

    CATEGORY_CHOICES = [
        ('main', 'Головна'),
        ('important', 'Важливі місця'),
        ('cabinet', 'Кабінети'),
    ]

    name = models.CharField(max_length=100, verbose_name="Назва")
    category = models.CharField(max_length=20, blank=True, null=True, choices=CATEGORY_CHOICES,
                                verbose_name="Категорія")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Опис")
    image = models.ImageField(upload_to=image_file_path, blank=True, null=True, verbose_name="Зображення (опціонально)")
    flight_type = models.CharField(max_length=20, blank=True, choices=FLIGHT_TYPE_CHOICES, default=None,
                                   verbose_name="Дiя камери")

    speed = models.FloatField(blank=True, null=True, verbose_name="Швидкість камери")
    camera_view_direction = models.CharField(max_length=10, choices=CAMERA_VIEW_DIRECTION_CHOICES, blank=True,
                                             null=True, verbose_name="Напрямок камери")
    camera_pitch = models.FloatField(blank=True, null=True, verbose_name="Нахил камери (pitch, Y), °")

    position_x = models.FloatField(blank=True, null=True, verbose_name="Позиція X")
    position_y = models.FloatField(blank=True, null=True, verbose_name="Позиція Y")
    position_z = models.FloatField(blank=True, null=True, verbose_name="Позиція Z")

    yaw = models.FloatField(blank=True, null=True, verbose_name="Азимут (yaw, X), °")
    pitch = models.FloatField(blank=True, null=True, verbose_name="Нахил (pitch, Y), °")

    def __str__(self):
        return f"{self.name} ({self.get_flight_type_display()})"

    class Meta:
        verbose_name = 'Локація обльоту'
        verbose_name_plural = 'Локації обльоту'


@receiver(post_delete, sender=FlightLocation)
def delete_image_file(sender, instance, **_kwargs):
    if instance.image:
        instance.image.delete(save=False)


class FlightPoint(models.Model):
    location = models.ForeignKey(FlightLocation, on_delete=models.CASCADE, related_name='flight_points')
    order = models.PositiveIntegerField(default=0)
    position_x = models.FloatField(verbose_name="Позиція X")
    position_y = models.FloatField(verbose_name="Позиція Y")
    position_z = models.FloatField(verbose_name="Позиція Z")

    def __str__(self):
        return f"Точка [{self.position_x}, {self.position_y}, {self.position_z}] для {self.location.name}"

    class Meta:
        ordering = ['id']
        verbose_name = 'Точка польоту'
        verbose_name_plural = 'Точки польоту'


class UniversityModel(models.Model):
    version = models.CharField(max_length=20, verbose_name="Версія", unique=True)
    model_file = models.FileField(upload_to=model_file_path, verbose_name="Файл моделі")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата завантаження")
    is_active = models.BooleanField(default=True, verbose_name="Активна модель")

    def save(self, *args, **kwargs):
        if self.is_active:
            UniversityModel.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.version} ({"Active" if self.is_active else "Inactive"})'

    class Meta:
        verbose_name = 'Модель університету'
        verbose_name_plural = 'Моделі університету'


@receiver(post_delete, sender=UniversityModel)
def delete_model_file(sender, instance, **_kwargs):
    if instance.model_file:
        instance.model_file.delete(save=False)

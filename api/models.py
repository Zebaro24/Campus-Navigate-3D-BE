from datetime import datetime
import os

from django.db import models


def model_file_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return f'models_3d/model_{instance.version}_{timestamp}{ext}'


class FlightLocation(models.Model):
    FLIGHT_TYPE_CHOICES = [
        ('static_frame', 'Статичний кадр'),
        ('points_flight', 'Обліт по точках'),
        ('panorama', 'Панорама навколо'),
    ]

    CAMERA_VIEW_DIRECTION_CHOICES = [
        ('inside', 'Дивитися всередину'),
        ('outside', 'Дивитися назовні'),
    ]

    name = models.CharField(max_length=100, verbose_name="Назва")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Опис")
    image = models.ImageField(upload_to='place_images/', blank=True, null=True, verbose_name="Зображення (опціонально)")
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
    roll = models.FloatField(blank=True, null=True, verbose_name="Крен (roll, Z), °")

    def __str__(self):
        return f"{self.name} ({self.get_flight_type_display()})"

    class Meta:
        verbose_name = 'Локація обльоту'
        verbose_name_plural = 'Локації обльоту'


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

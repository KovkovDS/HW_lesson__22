from django.core.exceptions import ValidationError


def validate_image_size(image):  # Укажите максимально допустимый размер изображения (в байтах)
    max_size = 5 * 1024 * 1024  # 2 МБ

    if image.size > max_size:
        raise ValidationError(" Размер загружаемого изображения должен быть меньше 5 МБ.")

from .models import Product, Category


class ListProductsCategories:

    @staticmethod
    def get_products_categories(category=None):
        # category = Category.objects.all()
        if category is None:
            products = Product.objects.all()
        else:
            products = Product.objects.all().filter(category=category)
        return products

    # @staticmethod
    # def calculate_average_grade(student_id):
    #     # Получаем все оценки студента
    #     grades = Grade.objects.filter(student_id=student_id)
    #     # Если оценок нет, возвращаем None
    #     if not grades.exists():
    #         return None

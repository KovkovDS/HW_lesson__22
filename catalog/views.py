from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from catalog.models import Product, Contact
from django.core.paginator import Paginator


def home(request):
    products = Product.objects.all()
    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')
    products_list = paginator.get_page(page_number)
    print(*products[:5])
    print(len(products))
    return render(request, 'home.html', {'products': products_list})


def contacts(request):
    try:
        contact = Contact.objects.get(id=1)
        return render(request, 'contacts.html',
                      {'legal_address': contact.legal_address, 'mailing_address': contact.mailing_address,
                       'email': contact.email, 'tel': contact.tel})
    except Contact.DoesNotExist:
        print('Ни каких контактных данных компании не найдено.')
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f'Спасибо, {name}, Ваше сообщение получено.')
    return render(request, 'contacts.html')


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'product.html', context)


def added_product(request, name_p):
    return render(request, 'added_product.html', {'name_p': name_p})


def adding_product(request):
    if request.method == 'POST':
        name_p = request.POST.get('name_p')
        price_by = request.POST.get('price_by')
        description_p =request.POST.get('description_p')
        picture = request.POST.get('picture')
        category_id = request.POST.get('category_id')
        new_product = Product.objects.create(name_p=name_p, price_by=price_by, description_p=description_p,
                                             picture=picture, category_id=category_id)
        request.method = 'GET'
        return added_product(request, name_p)
    return render(request, 'adding_product.html')

from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Product, Contact



def home(request):
    five_latest_products = Product.objects.all()[:5]
    print(*five_latest_products)
    return render(request, 'home.html', {'five_latest_products_зфк_1': five_latest_products[:2],
                                         'five_latest_products_зфк_2': five_latest_products[2:5]})


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
    product = Product.objects.get(id=product_id)
    context = {'product': product}
    return render(request, 'product_detail.html', context)
from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Product, Contact

# Create your views here.

def home(request):
    five_latest_products = Product.objects.all()[0:5]
    print(*five_latest_products)
    #request = Product.objects.latest('-create_at')
    return render(request, 'home.html', {'product_1': five_latest_products[0],
                                         'product_2': five_latest_products[1], 'product_3': five_latest_products[2],
                                         'product_4': five_latest_products[3], 'product_5': five_latest_products[4]})

def contacts(request):
    try:
        contact = Contact.objects.get(id=1)
        return render(request, 'contacts.html',
                      {'legal_address': contact.legal_address, 'mailing_address': contact.mailing_address,
                       'email': contact.email, 'tel': contact.tel})
    except Contact.DoesNotExist:
        print(f'Ни каких контактных данных компании не найдено.')
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f'Спасибо, {name}, Ваше сообщение получено.')
    return render(request, 'contacts.html')

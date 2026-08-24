from django.shortcuts import render
from .models import Coffee, Order, OrderItem, Feedback


def home(request):
    return render(request, 'home.html')



def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        rating = request.POST.get('rating')
        message = request.POST.get('message')
        Feedback.objects.create(
            name=name,
            email=email,
            rating=rating,
            message=message)
        return render(request,'feedback_success.html')
    return render(request,'feedback.html')



def about(request):
    return render(request, 'about.html')



def order_ahead(request):
    coffees = Coffee.objects.filter(
        is_available=True)


    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        pickup_time = request.POST.get('pickup_time')
        instructions = request.POST.get('instructions')
        coffee_ids = request.POST.getlist('coffee')
        quantities = request.POST.getlist('quantity')


        order = Order.objects.create(
            name=name,
            phone=phone,
            pickup_time=pickup_time,
            instructions=instructions
        )


        for coffee_id, quantity in zip(
            coffee_ids,
            quantities
        ):

            coffee = Coffee.objects.get(
                id=coffee_id
            )

            OrderItem.objects.create(
                order=order,
                coffee=coffee,
                quantity=quantity,
                price=coffee.price
            )
        return render(request,'order_success.html',{'order': order})
    return render(request,'order_ahead.html',{'coffees': coffees})



def menu(request):
    coffees = Coffee.objects.filter(is_available=True)
    search = request.GET.get('search', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort = request.GET.get('sort', '')
    if search:
        coffees = coffees.filter(name__icontains=search)
    if min_price:
        coffees = coffees.filter(price__gte=min_price)
    if max_price:
        coffees = coffees.filter(price__lte=max_price)
    if sort == 'price_low':
        coffees = coffees.order_by('price')
    elif sort == 'price_high':
        coffees = coffees.order_by('-price')
    elif sort == 'name_az':
        coffees = coffees.order_by('name')
    elif sort == 'name_za':
        coffees = coffees.order_by('-name')
    else:
        coffees = coffees.order_by('price')
    return render(request,'menu.html',
        {
            'coffees': coffees,
            'search': search,
            'min_price': min_price,
            'max_price': max_price,
            'sort': sort,
        }
    )
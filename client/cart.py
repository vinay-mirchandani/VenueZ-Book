from decimal import Decimal
from django.conf import settings
from fly.models import Hall

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, Hall, quantity=1, update_quantity=False):
        hall_id = str(Hall.hall_id)
        if hall_id not in self.cart:
            self.cart[hall_id] = {'id':Hall.hall_id,'quantity': 0,'name':Hall.hall_name, 'contact': Hall.contact}
        if update_quantity:
            self.cart[hall_id]['quantity'] = quantity
        else:
            self.cart[hall_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, Hall):
        hall_id = str(Hall.hall_id)
        if hall_id in self.cart:
            del self.cart[hall_id]
            self.save()

    def __iter__(self):
        hall_ids = self.cart.keys()
        hall = Hall.objects.filter(hall_id__in=hall_ids)
        for product in hall:
            self.cart[str(product.prd_id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
from django.core.handlers.wsgi import WSGIRequest


class CartService():
    def __init__(self, request: WSGIRequest):
        self.request = request


    def get_cart(self):
        pass

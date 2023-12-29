from pprint import pprint

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.views import View

from apps.site.site_product.filter import ProductFilter
from apps.site.site_product.models import ShopProductModel, ShopTypeModel, ShopKeyModel

from django.template import Engine




class CategoryView(View):

    def get(self, request: WSGIRequest, category=None):

        category_carousel = ShopTypeModel.objects.all()
        keys = ShopKeyModel.objects.filter(value=category)
        products = ShopProductModel.objects.filter(
            id__in=[i.product.id for i in keys])
        form = ProductFilter(request.GET, queryset=products)

        product_keys = []
        for i in products:
            product_keys.append(
                ShopKeyModel.objects.filter(product=i).values('key', 'value')
            )
        out = {}
        keys_list = []
        for i in product_keys:
            for j in i:
                if j['key'] != 'slug':
                    if j['key'] not in out:
                        out[j['key']] = []
                    if j['value'] not in out[j['key']]:
                        out[j['key']].append(j['value'])
                    if j['key'] not in keys_list:
                        keys_list.append(j['key'])
        selected_values = [i for i, v in request.GET.items() if i != 'csrfmiddlewaretoken']
        return render(
            request=request,
            template_name='html/site/category.html',
            context={
                'filter': form,
                'category_carousel': category_carousel,
                'keys': keys_list,
                'dictionary': out,
                'selected_values': selected_values,
            })


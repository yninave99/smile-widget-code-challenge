from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from products.models import Product, GiftCard, ProductPrice
import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def get_product_price(request):
    """
        Fetches the Product Amount including Name and Product Code
        @@ ---------------------------------------------------
            Input : Rest Request with productid, date and giftcode
            Type : Get
            Output : 
                Onsuccess : 1) Message : Success
                            2) Data : List of Product Price
                Onerror   : 1) Message : Failed
                            2) Data : Empty List
    """
    product_id = None if request.GET['productid'].lower() == 'all' else request.GET['productid']
    date = request.GET['date']

    try:
        # Get Product amount w.r.t prod_id and date
        product_list = get_product_amount(date, product_id)

        gift_code = request.GET['giftcode']
        for product in product_list:
            if not gift_code.lower() == "all":
                discount_amt = get_discount_amount(gift_code, date)
                product['amount'] = product['amount'] - discount_amt
                product['amount'] = product['amount'] if product['amount'] > 0 else 0
        return Response({'message' : "success", "data": product_list})
    except Exception as e:
        return Response({'message' : "Failed", "data":[]})

@api_view()
def get_product_code(request):
    """
        Fetches the Product Code
        @@ ---------------------------------------------------
            Input : Rest Request
            Type : Get
            Output : 
                Onsuccess : 1) Message : Success
                            2) Data : List of Products
                Onerror   : 1) Message : Failed
                            2) Data : Empty List
    """
    try:
        products = Product.objects.all().values()
        products_list = list(products)
        return Response({'message' : "success", "data":products_list})
    except Exception as e:
        return Response({'message' : "Failed", "data":[]})


@api_view()
def get_gift_code(request):
    """
        Fetches the Gift Card Code
        @@ ---------------------------------------------------
            Input : Rest Request
            Type : Get
            Output : 
                Onsuccess : 1) Message : Success
                            2) Data : List of Gift Codes
                Onerror   : 1) Message : Failed
                            2) Data : Empty List
    """
    try:
        gift_card = GiftCard.objects.all().values()
        gift_list = list(gift_card)
        return Response({'message' : "success", "data":gift_list})
    except Exception as e:
        return Response({'message' : "Failed", "data":[]})


def create_product_list(productQueryObj):
    """
        Create Final Product list to be send to Frontend
    """
    try:
        product_list = []
        for product in productQueryObj:
            temp_dict = {}
            if 'amount' in product:
                product_obj = Product.objects.get(id=product['product_id_id'])
                temp_dict['amount'] = product['amount']
                temp_dict['id'] = product['product_id_id']
                temp_dict['product_name'] = product_obj.name
                temp_dict['product_code'] = product_obj.code
                temp_dict['price_schedule'] = product['price_schedule']
            else:
                temp_dict['amount'] = product['price']
                temp_dict['id'] = product['id']
                temp_dict['product_name'] = product['name']
                temp_dict['product_code'] = product['code']
                temp_dict['price_schedule'] = None

            product_list.append(temp_dict)
        return product_list
    except Exception as e:
        return False


def get_product_amount(date, productId=None):
    """
    Fetches the Product Amount Based on the Dates and Product Code given
    """
    try:
        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        if productId is not None:
            product_query_obj = ProductPrice.objects.filter(product_id=productId, date_start__lte=date_time_obj).values()
            product_list = []
            for product in product_query_obj:
                if product['date_end'] is not None:
                    if product['date_start'] <= date_time_obj and product['date_end'] >= date_time_obj:
                        product_list.append(product)
                else:
                    if product['date_start'] <= date_time_obj:
                        product_list.append(product)

            if not len(product_list):
                product_list = Product.objects.filter(id=productId).values()
        else:
            product_query_obj = ProductPrice.objects.filter(date_start__lte=date_time_obj).values()
            product_list = []
            for product in product_query_obj:
                if product['date_end'] is not None:
                    if product['date_start'] <= date_time_obj and product['date_end'] >= date_time_obj:
                        product_list.append(product)
                else:
                    if product['date_start'] <= date_time_obj:
                        product_list.append(product)

            if not len(product_list):
                product_list = Product.objects.filter().values()

        return create_product_list(product_list)

    except Exception as e:

        return False


def get_discount_amount(giftCardCode, date):
    """
        Fetches the Discount Amount for user based on its gift card validity
    """
    try:
        discount_amt = 0
        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        gift_card_obj = GiftCard.objects.filter(id=giftCardCode, date_start__lte=date_time_obj).values()

        if len(gift_card_obj):
            gift_card_obj = gift_card_obj[0]
            if gift_card_obj['date_end'] is not None:
                if gift_card_obj['date_start'] <= date_time_obj and gift_card_obj['date_end'] >= date_time_obj:
                    discount_amt = gift_card_obj['amount']
            else:
                if gift_card_obj['date_start'] <= date_time_obj:
                    discount_amt = gift_card_obj['amount']

        return(discount_amt)

    except Exception as e:
        
        return False

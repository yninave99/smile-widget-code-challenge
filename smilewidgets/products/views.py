from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from products.models import Product, GiftCard, ProductPrice
import datetime


def index(request):
    """
        Render Homepage
    """
    return render(request, 'index.html', {"title": "home"})


def get_product_price(request):
    """
        Fetches the Product Amount including Name and Product Code
    """
    productId = None if request.GET['productid'] == 'All' else request.GET['productid']
    date = request.GET['date']

    try:
        # Get Product amount w.r.t prod_id and date
        productListWithAmount = get_product_amount(date, productId)

        giftcode = request.GET['giftcode']
        for product in productListWithAmount:
            if not giftcode == "All":
                discountAmt = getDiscountAmount(giftcode, date)
                product['amount'] = product['amount'] - discountAmt
                product['amount'] = product['amount'] if product['amount'] > 0 else 0
        return JsonResponse(productListWithAmount, safe=False)
    except Exception as e:
        return(JsonResponse("Error Occured", safe=False))


def get_product_code(request):
    """
        Fetches the Product Code
    """
    try:
        products = Product.objects.all().values()
        products_list = list(products)
        return JsonResponse(products_list, safe=False)
    except Exception as e:
        return(JsonResponse("Error Occured", safe=False))



def get_gift_code(request):
    """
        Fetches the Gift Card Code
    """
    try:
        gift_card = GiftCard.objects.all().values()
        gift_list = list(gift_card)
        return JsonResponse(gift_list, safe=False)
    except Exception as e:
        return(JsonResponse("Error Occured", safe=False))


def createProductList(productQueryObj):
    """
        Create Final Product list to be send to Frontend
    """
    try:
        productListWithAmount = []
        for product in productQueryObj:
            tempDict = {}
            if 'amount' in product:
                tempDict['amount'] = product['amount']
                tempDict['id'] = product['product_id_id']
                tempDict['product_name'] = Product.objects.get(id=product['product_id_id']).name
                tempDict['product_code'] = Product.objects.get(id=product['product_id_id']).code
            else:
                tempDict['amount'] = product['price']
                tempDict['id'] = product['id']
                tempDict['product_name'] = product['name']
                tempDict['product_code'] = product['code']

            productListWithAmount.append(tempDict)
        return productListWithAmount
    except Exception as e:
        return False


def get_product_amount(date, productId=None):
    """
    Fetches the Product Amount Based on the Dates and Product Code given
    """
    try:
        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        if productId is not None:
            productQueryObj = ProductPrice.objects.filter(product_id=productId, date_start__lte=date_time_obj).values()
            productQuery = []
            for element in productQueryObj:
                if element['date_end'] is not None:
                    if element['date_start'] <= date_time_obj and element['date_end'] >= date_time_obj:
                        productQuery.append(element)
                else:
                    if element['date_start'] <= date_time_obj:
                        productQuery.append(element)

            if not len(productQuery):
                productQuery = Product.objects.filter(id=productId).values()
        else:
            productQueryObj = ProductPrice.objects.filter(date_start__lte=date_time_obj).values()
            productQuery = []
            for element in productQueryObj:
                if element['date_end'] is not None:
                    if element['date_start'] <= date_time_obj and element['date_end'] >= date_time_obj:
                        productQuery.append(element)
                else:
                    if element['date_start'] <= date_time_obj:
                        productQuery.append(element)

            if not len(productQuery):
                productQuery = Product.objects.filter().values()
        return createProductList(productQuery)
    except Exception as e:
        return False


def getDiscountAmount(giftCardCode, date):
    """
        Fetches the Discount Amount for user based on its gift card validity
    """
    try:
        discountAmt = 0
        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        giftCardObj = GiftCard.objects.filter(id=giftCardCode, date_start__lte=date_time_obj).values()
        if len(giftCardObj):
            giftCardObj = giftCardObj[0]
            if giftCardObj['date_end'] is not None:
                if giftCardObj['date_start'] <= date_time_obj and giftCardObj['date_end'] >= date_time_obj:
                    discountAmt = giftCardObj['amount']
            else:
                if giftCardObj['date_start'] <= date_time_obj:
                    discountAmt = giftCardObj['amount']
        return(discountAmt)
    except Exception as e:
        return False

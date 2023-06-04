import requests
from bs4 import BeautifulSoup
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse


@api_view(["GET"])
def mercadoLibre(request):
    product = request.GET.get('product')

    if product:
        url = f'https://listado.mercadolibre.com.co/{product}'
        response = requests.get(url)

        if response.status_code == 200:
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')
            # Localizes the main container of the products
            box = soup.find(
                'ol', class_='ui-search-layout ui-search-layout--stack shops__layout')

            # Localizes the list of products
            products = box.find_all(
                'li', class_='ui-search-layout__item shops__layout-item')

            # Gets the product name
            def productName(tag):
                return tag.find('h2', class_='ui-search-item__title shops__item-title').get_text()

            # Gets the product price
            def productPrice(tag):
                return tag.find('div', class_='ui-search-price__second-line shops__price-second-line').find(
                    'span', class_='price-tag-text-sr-only').get_text().split()[0]

            # Gets the product image
            def productImage(tag):
                return tag.find('img').get('data-src')

            # Gets the product url
            def productUrl(tag):
                return tag.find('a', class_='ui-search-link').get('href')

            # Creates the objects
            productNames = [{'name': productName(i), 'price': productPrice(i), 'image': productImage(i), 'url': productUrl(i)}
                            for i in products[:]]

            return JsonResponse(productNames, status=status.HTTP_200_OK, safe=False)

        else:
            # If the request was not successful an error response is returned.
            return JsonResponse({'error': 'Error en la solicitud'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        # If a "product" field is not provided an error response is returned.
        return JsonResponse({'error': 'The "product" field is required'}, status=status.HTTP_400_BAD_REQUEST)

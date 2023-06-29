import requests
from .pagination import CustomPagination
from bs4 import BeautifulSoup
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json


@api_view(["GET"])
def searchProduct(request):
    product = request.GET.get('product')

    if product:
        mercadoLibreProducts = mercadoLibre(product)
        loPidoProducts = loPido(product)
        tiendeoProducts = tiendeo(product)
        laCesteriaProducts = laCesteria(product)

        # Combines the scraping of the different sites
        products = laCesteriaProducts + loPidoProducts + tiendeoProducts + mercadoLibreProducts

        # If the request was unsuccessful an error response is returned.
        if not products:
            return JsonResponse({'error': 'Request error'}, status=status.HTTP_404_NOT_FOUND)

        else:
            paginator = CustomPagination()
            paginated_products = paginator.paginate_queryset(products, request)
            return paginator.get_paginated_response(paginated_products)


    else:
        # If a "product" field is not provided an error response is returned.
        return JsonResponse({'error': 'The product field is required'}, status=status.HTTP_400_BAD_REQUEST)


def mercadoLibre(product):
    url = f'https://listado.mercadolibre.com.co/{product}'
    response = requests.get(url)

    if response.status_code == 200:
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

        try:
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
            productNames = [{'name': productName(i), 'price': productPrice(i), 'image': productImage(i),
                             'url': productUrl(i), 'store': 'Mercado Libre'}
                            for i in products[:20]]

            return productNames

        except (AttributeError, TypeError):
            return []

    else:
        return []


def loPido(product):
    url = f'https://www.lopido.com/{product}?_q={product}&map=ft'
    response = requests.get(url)

    if response.status_code == 200:
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

        try:
            # Checks if the search returned results
            notFound = soup.find(
                'span', class_='vtex-search-result-3-x-searchNotFoundTextListLine c-muted-1 b')

            if notFound:
                return []

            # Localizes the main container of the products
            box = soup.find('div', class_='flex flex-column min-vh-100 w-100'
                            )
            boxScript = box.find(
                'script', type="application/ld+json").get_text()

            dictData = json.loads(boxScript)

            productNames = [{'name': product['item']['name'], 'price': product['item']['offers']['offers'][0]['price'],
                             'image': product['item']['image'], 'url': product['item']['@id'],
                             'store': 'Lopido.com'}
                            for product in dictData['itemListElement'][:16]]

            return productNames

        except (AttributeError, TypeError):
            return []

    else:
        return []


def tiendeo(product):
    url = f'https://www.tiendeo.com.co/ofertas/{product}'
    response = requests.get(url)

    if response.status_code == 200:
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

        try:
            # Localizes the main container of the products
            box = soup.find(
                'section', class_='sc-bRlCZA hlYIsl js-print-article-container js-print-container')

            # Localizes the list of products
            products = box.find('section', role='region').find(
                'ul', class_='sc-edLOhm fkWkqK').find_all(
                'li', class_='sc-jmfXTE eXDiee')

            # Gets the product name
            def productName(tag):
                return tag.find('h3').get_text()

            # Gets the product price
            def productPrice(tag):
                priceDiv = tag.find(
                    'div', class_='sc-4e35cfdd-0 sc-4e35cfdd-3 sc-234eed98-13 sc-a4883c8d-9 '
                    'kxnaJu hyLhly hnZwKt fmetNz').get_text()

                price = priceDiv.split('$')[1] if priceDiv else '0'
                return price

            # Gets the product image
            def productImage(tag):
                return tag.find('div', class_='sc-234eed98-4 sc-a4883c8d-2 bjExpC cJLFLA').find(
                    'img').get('src')

            # Gets the product url
            def productUrl(tag):
                hasUrl = tag.find(
                    'a', class_='sc-a4883c8d-0 ecBHID')

                if hasUrl:
                    return hasUrl.get('href')

                else:

                    article = tag.find(
                        'article', class_='sc-234eed98-0 sc-a4883c8d-1 qpzBM hIUzyD products '
                        'js-print-article-item')

                    catalogId = article.get('data-idcatalog')
                    productId = article.get('data-id')

                    url = f'https://www.tiendeo.com.co/Catalogos/{catalogId}?priorElementId={productId}'
                    return url

            # Creates the objects
            productNames = [{'name': productName(i), 'price': productPrice(i), 'image': productImage(i),
                             'url': productUrl(i), 'store': 'Tiendeo'}
                            for i in products[:12]]
            return productNames

        except (AttributeError, TypeError):
            return []

    else:
        return []


def laCesteria(product):
    url = 'https://lacesteria.co/search?type=product&options%5Bprefix%5D=last&options%5Bunavailable_'\
        f'products%5D=hide&q={product}'

    response = requests.get(url)

    if response.status_code == 200:
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

        try:
            # Localizes the main container of the products
            box = soup.find(
                'div', class_='product-list product-list--collection')

            # Localizes the list of products
            products = box.find_all(
                'div', class_='product-item product-item--vertical 1/3--tablet-and-up 1/4--desk')

            # Gets the product name
            def productName(tag):
                return tag.find('a', class_='product-item__title text--strong link').get_text()

            # Gets the product price
            def productPrice(tag):
                priceWithPoint = tag.find('div', class_='product-item__price-list price-list').find(
                    'span', class_='price').get_text().split('$')[1]

                price = int(priceWithPoint.replace('.', ''))

                return price

            # Gets the product image
            def productImage(tag):
                return 'https:' + tag.find('noscript').find('img').get('src')

            # Gets the product url
            def productUrl(tag):
                return 'https://lacesteria.co' + tag.find('a', class_='product-item__title text--strong link').get('href')

            # Creates the objects
            productNames = [{'name': productName(i), 'price': productPrice(i), 'image': productImage(i),
                             'url': productUrl(i), 'store': 'La Cestería'}
                            for i in products[:24]]

            sorted_products = sorted(productNames, key=lambda x: int(x["price"]) if isinstance(x["price"], int) else int(x["price"]))

            return sorted_products

        except (AttributeError, TypeError):
            return []

    else:
        return []

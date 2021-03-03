import requests
import time
import json

from django.shortcuts import render
from json import loads, dumps
from collections import OrderedDict
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.conf import settings
from rest_framework.response import Response
from books.models import BookInventory
from books.serializers import BooksSerializer
from rest_framework.decorators import api_view

"""
This module is used to perrform CRUD operation to the database
"""
@api_view(['GET', 'POST'])
def books_list(request):
    if request.method == 'GET':
        #check whether the request object contains the title parameter
        title = request.query_params.get('title', None)
        #Get all the Book Details existing in database
        book_data = getBookData()
        inventoryDict = dict()
        bookData = list()
        #When the title is not empty/None
        if title is not None:
            #create a new dict of inventory
            for item in book_data:
                inventoryDict[item['bookid']] = item['quantity']
            #Get the details based on the input title
            response = books_search(title)
            for data in response['items']:
                #initialize the quantity as zero for all books
                quantity = 0
                #check whether the bookid exists in database
                bookExists = getBookId(data)
                #IF the bookid exists in database update the quantity accordingly
                if  bookExists in inventoryDict.keys():
                    quantity = inventoryDict[bookExists]
                #New list of dict is generated
                bookData.append({
                    "title":getTitle(data),
                    "link":getLink(data),
                    "thumbnail":getThumbnail(data),
                    "quantity":quantity
                })
                #The old list of dict is overwritten with new data
                book_data = bookData
        else:
            #when the title is empty consider the data in inventory
            for data in range(len(book_data)):
                response = get_book_data_by_id(book_data[data].get('bookid'))
                #when response is not empty
                if response != '':
                    book_data[data].update({'title':getTitle(response)})
                    book_data[data].update({'link':getLink(response)})
                    book_data[data].update({'thumbnail':getThumbnail(response)})
        return JsonResponse(book_data,safe=False)
    
    elif request.method == 'POST':
        #parse the request object and store it as JSON
        book_data = JSONParser().parse(request)
        #Convert the JSON to Object
        book_serializer = BooksSerializer(data=book_data)
        #check whether the created object is valid
        if book_serializer.is_valid():
            book_serializer.save()
            #return 201 when the objects gets created in database
            return JsonResponse(book_serializer.data, status=status.HTTP_201_CREATED) 
        #if there is a failure return as bad request
        return JsonResponse(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
This module is used to get Book data based on ID
I/P - BookId
O/P - JSON data from the API
"""
def get_book_data_by_id(bookid):
    try:
        r = requests.get(settings.GOOGLE_BOOKS_API_URL+bookid, timeout=10)
        data = ''
        if r.status_code == 200:
            data = r.json()
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print (e.response.text)

    return data

"""
This module is used to search books based on title
i/p title
o/p JSON data
"""
def books_search(title):
    try:
        r = requests.get(settings.GOOGLE_BOOKS_API_URL+"?q="+title, timeout=10)
        data = ''
        if r.status_code == 200:
            data = r.json()
    except requests.exceptions.HTTPError as e:
        print (e.response.text)
    return data

"""
This is used to extract title from JSON
"""
def getTitle(response):
    return response.get('volumeInfo',{}).get('title')

"""
This is used to extract link from JSON
"""
def getLink(response):
    return response.get('volumeInfo',{}).get('infoLink')

"""
This is used to extract thumbnail from JSON
"""
def getThumbnail(response):
    return response.get('volumeInfo',{}).get('imageLinks',{}).get('thumbnail')

"""
This is used to extract bookid from JSON
"""
def getBookId(response):
    return response.get('id')


"""
This module provides all the existing data in db
"""
def getBookData():
    books = BookInventory.objects.all()
    books_serializer = BooksSerializer(books, many=True)
    #convert orderd dict to dict
    book_data = loads(dumps(books_serializer.data))
    return book_data

"""
This module is used to perform various operattions on indivisual entities
"""
@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):
    try:
        bookInventory = BookInventory.objects.get(pk=pk) 
    except BookInventory.DoesNotExist: 
        return JsonResponse({'message': 'The BookInventory does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET': 
        books_serializer = BooksSerializer(bookInventory) 
        return JsonResponse(books_serializer.data) 
    #update the existing data in database
    elif request.method == 'PUT': 
        book_data = JSONParser().parse(request)
        books_serializer = BooksSerializer(bookInventory, data=book_data) 
        if books_serializer.is_valid(): 
            books_serializer.save() 
            return JsonResponse(books_serializer.data) 
        return JsonResponse(books_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    #delete the book in database
    elif request.method == 'DELETE': 
        bookInventory.delete() 
        return JsonResponse({'message': 'BookInventory was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
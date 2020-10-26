"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from . import fetch

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def searchQuery(request):
    assert isinstance(request, HttpRequest)

    queryTerm = request.POST.get('searchTerm')
    if queryTerm == "":
        queryTerm = " "
    
    searchByPerson = request.POST.get('searchByPerson')
    
    stuff = fetch.fetch.fetch_all_tvshows(queryTerm)        
    tvShowPosters = stuff[0]
    tvShowIDs = stuff[1]
    tvShowTitle = stuff[2]

    return render(
        request,
        'app/layout.html',
        {
            'title':'TV Shows',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'showDetails': zip(tvShowPosters,tvShowIDs,tvShowTitle),
        }
    )
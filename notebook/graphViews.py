# views file for graphs
from django.db import connections
from django.db.models import Count, Sum
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from numpy.testing._private.utils import jiffies
import pandas as pd 
from datetime import datetime 
import json

from .models import Program

#View for the main graph page
def graph(request):
    return render(request, 'graphs/graph.html')


#Return programs data grouped by provider by year as json
def programs_count_by_provider(request):
    data = Program.objects.all() \
        .values('providers__provider_name', 'release_date__year') \
        .annotate(count_name=Count('id')) \
        .order_by()


    providers_byYear = dict()
    max_year = 0
    min_year = datetime.now().year

    for row in list(data):
        min_year = int(row['release_date__year']) if int(row['release_date__year']) < min_year else min_year
        max_year = int(row['release_date__year']) if int(row['release_date__year']) > max_year else max_year

        if(row['providers__provider_name'] not in providers_byYear.keys() ):
            providers_byYear[row['providers__provider_name']] = None 
    

    index_year = dict()
    j = 0
    for i in range(min_year, max_year):
        index_year[i] = j
        j+= 1
    index_year[max_year] = j

    for key in providers_byYear.keys():
        providers_byYear[key] = [0] * len(index_year.keys())
    
    providers_byYear['Year'] = list(index_year.keys())

    for row in list(data):
        index = index_year[int(row['release_date__year'])]
        providers_byYear[row['providers__provider_name']][index] = row['count_name'] * 10000

         
    
    df = pd.DataFrame(providers_byYear)
    #return JsonResponse(list(providers_byYear), safe=False)
    #return JsonResponse(list(data), safe=False)
    return HttpResponse(
        df.to_csv(index=False, line_terminator="\n", encoding='utf-8'),
        )
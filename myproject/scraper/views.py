from django.shortcuts import render, HttpResponse, redirect
import subprocess
from django.urls import reverse

from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys

# Create your views here.
def home(request):
    if request.method == "POST":
        your_url = request.POST.get('urlname', None)
        table_num = request.POST.get('tablenumname', None)
        args = scrap(your_url, table_num)
        return render(request, "home.html", args)
    return render(request, "home.html")

def scrap(your_url, table_num):
    args = {}
    try:
        df = data_scraper(your_url, table_num)
        #print(type(result))
        args['mytext'] = df
        #df = pd.read_csv(StringIO(str(result.stdout)),engine ='python', sep=r"\s\s+")
        #print(df)
        #print(df)
        #column_names = list(df.columns.values)
        #print(column_names)
        #args['header'] = [df.set_index('Rank').T.to_dict('list')]
        
        #print(type(df.to_dict()))
        #args['rows'] = [{'id':1, 'chemblid':534988,'prefName':'A'},
        #                   {'id':2, 'chemblid':31290,'prefName':'B'},
        #                   {'id':3, 'chemblid':98765,'prefName':'C'}]
    except:
        args['mytext'] = str("Enter url")
    #print("DONE DONE DONE DONE DONE")
    return args


def data_scraper(your_url, table_num):
    #url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'
    #url = 'http://sebastianbrzustowicz.pythonanywhere.com/about_me'
    #url = 'https://info.cern.ch/'

    url = str(your_url)
    table_num = int(table_num)

    #if len(sys.argv) > 1:
    #    url = str(sys.argv[1])
    #    table_num = int(sys.argv[2])

    #url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'#

    page = requests.get(url).text

    soup = BeautifulSoup(page, "html.parser")

    table = soup.find_all('table')[table_num]
    world_titles = table.find_all('th')
    world_table_titles = [title.text.strip() for title in world_titles]

    df = pd.DataFrame(columns = world_table_titles)

    column_data = table.find_all('tr')

    for row in column_data[1:]:
        row_data = row.find_all('td')
        individual_row_data = [data.text.strip() for data in row_data]

        length = len(df)
        df.loc[length] = individual_row_data

    #print(df)
    #df = df.reset_index(drop=True)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 10000)

    df = df.to_string(index=False)
    #print(df)
    #print(df.to_string(index=False))
    return df
    #return df.to_string(index=False)
    #return df.set_index('#').T.to_dict('list')
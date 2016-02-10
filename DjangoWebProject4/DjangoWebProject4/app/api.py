'''
The djurassic service api.

Cheers, Nels
'''

#### Django modules
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseServerError, HttpResponseNotFound
from django.template import RequestContext
from django.views.decorators.cache import cache_control
from django.conf import settings

#### External modules
from io import BytesIO
import datetime
#import dateutil.parser
import json
import mimetypes, os
import tempfile
import pandas as pd
#import numpy as np
#import numpy.ma as ma
#from scipy.interpolate import interp1d
#from matplotlib import mlab
#from azure.storage import BlobService, TableService
#import pyproj

#### Internal modules
#import tools.builder as b
#from settings import *
#import cannedresponses as cr
#from tools.drawing import *
#from tools import zfun
#from tools.blobcache import BlobCache
#from tools.fieldtable import FieldManager
#from app.settings import *

from azure.storage.blob import BlobService
import sys,re, string, json, os, subprocess, tempfile

def music(request):
    '''
    Random Quotes

    Expects an integer argument to message, not less than 0 not more than TIAS.
    That is the indexing starts from Zero.
    '''
    assert isinstance(request, HttpRequest)
    try:
        index = int(request.GET.get("message"))
        Quotes=["Folks we have trouble right here in River City and that starts with T and that rhymes with P and that stands for POOL!!!!", "That's not right. That's not even wrong.", "It takes a while before you sound like yourself.", "That's Adler's problem."]
        return HttpResponse(Quotes[index])
    except:
        return HttpResponseNotFound(content="You must provide a valid argument such as message=0 in your query URL. Either the index was out of range, wasn't an integer, or it was omitted entirely.")


def getblob(request):
    assert isinstance(request, HttpRequest)
    blob_service = BlobService(account_name='araldrift', account_key='otLzzkwQHQD3xFTQxwxy64PCL6eDINWGjSB7x6Ta2XVw3+3ffI5O2MhAEavf/r8qIW4G/dKrZAVg1R64nK7hDQ==')
    # http://<storage-account-name>.blob.core.windows.net/<container-name>/<blob-name>
    name = 'test.txt'
    fpath = '{0}\{1}'.format(tempfile.gettempdir(),name)
    blob_service.get_blob_to_path('flow', 'NARYN.day', fpath)
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=test.txt'
    blob.Properties.ContentDisposition = "attachment; filename=" + downloadName;
    return response

def gethydrograph(request):
    '''
    JSON return of a particular hydorgaph by start / stop / station / time interval

    In response it will 
        generate a 404 error if the value is not found
        or
        return a JSON response with the requested slice.
    '''
    assert isinstance(request, HttpRequest)
    
    start  = request.GET.get('start', None)
    end = request.GET.get('end', None)
    station = request.GET.get('station',None)
    interval  = request.GET.get('interval',None)

    #start blob service
    stationfile = station + '.day.new'
    blob_service = BlobService(account_name='araldrift', account_key='otLzzkwQHQD3xFTQxwxy64PCL6eDINWGjSB7x6Ta2XVw3+3ffI5O2MhAEavf/r8qIW4G/dKrZAVg1R64nK7hDQ==')
    blob_service.get_blob_to_path('flow', stationfile, './tmp.csv')  
    f = file('./tmp.csv')
    
    #read in pandas data and subsetting
    d_cols = ["date","flow"]
    d = pd.read_csv('./tmp.csv', sep=" ", names=d_cols)
    df = d[(d.date >= start) & (d.date <= end)] 
    h = df.to_json(orient='records')
    #h = []
    #while True:
     #   line = f.readline()
      #  if line == "": break
       # h.append(line)
    #f.close()
    json_encoded_result = json.dumps(h)

    try:
        return HttpResponse(json_encoded_result, content_type="application/json" )
    except Exception as a:
        return HttpResponseNotFound(content="No dice, either the inputs were out of range, the file couldn't be retrieved, or the winds weren't in your favor.")


    

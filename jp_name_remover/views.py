import urllib
import xml.etree.ElementTree as et

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages

from http import cookies

from secrets import token_urlsafe
from .classes.jp_name_remover import JpNameRemover

def home(request):
  if request.method == 'POST' and request.FILES['inputFile']:
    try:
      input_file = request.FILES['inputFile']
      input_file_filename = request.FILES['inputFile'].name
      received_rand_token = request.POST.get("rand_token", "")

      remover = JpNameRemover()
      output, remove_records = remover.remove_japanese_name(input_file)

      output_str = et.tostring(output, encoding='utf-8', method='xml')

      response = HttpResponse(output_str)
      response['Content-Disposition'] = 'attachment; filename=' + input_file_filename
      response.set_cookie("downloadToken", received_rand_token)
      return response
    except:
      return render(request, 'jp_name_remover/home.html', { 'error': 'REMOVE_ERROR' })
  else:
    return render(request, 'jp_name_remover/home.html')
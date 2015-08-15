# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.


def basecol1(request):
	return render(request, 'base-1col.html')
	
def basecol21(request):
	return render(request, 'base-2col1.html')

def basecol22(request):
	return render(request, 'base-2col2.html')

def basecol3(request):
	return render(request, 'base-3col.html')



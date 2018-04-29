from django.shortcuts import render
from django.http import  HttpResponse

from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company

# Create your views here.
def company_article_list(request):
	return render(request, 'finance/plotly.html', {})


class ChartData(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):
		articles = dict()
		for company in Company.objects.all():
			if company.articles > 0:
				articles[company.name] = company.articles
        #sorted returns a list eg:[('google':12),('yahoo':5),('amazon':8),etc] where the
        #key is used when we want how the list is to be sorted, here key = len always
        #where len is the in-built python func so when it says key = lambda x: x[1]
        #it means to sort the list according to low to high of the 2nd item
        #eg: after sorted it becomes like this [('yahoo':5),('amazon':8),('google':13),etc]
		articles = sorted(articles.items(), key=lambda x: x[1])
		articles = dict(articles)#this converts list to dict

		data = {
		    "article_labels":articles.keys(),
		    "article_data":articles.values(),
		}

		return Response(data)


def dash(request, **kwargs):
	return HttpResponse(dispatcher(request))

@csrf_exempt
def dash_ajax(request):
	return HttpResponse(dispatcher(request), content_type='application/json')
from django.shortcuts import render, redirect
import math
import requests
requests.packages.urllib3.disable_warnings()

from bs4 import BeautifulSoup
from datetime import timedelta, timezone, datetime
import os
import shutil

from .models import Headline, UserProfile
# Create your views here.

def news_list(request):
	#usr can only scrape once in 24hrs
	user_p = UserProfile.objects.filter(user=request.user).first()
	now = datetime.now(timezone.utc)
	time_diff = now - user_p.last_scrape
	time_diff_in_hrs = time_diff / timedelta(minutes=60)
	next_scrape = 24 - time_diff_in_hrs
	if time_diff_in_hrs <= 24:
		hide_me = True
	else:
		hide_me = False

	Headlines = Headline.objects.all()
	context = {
	'Headlines':Headlines, 
	'hide_me':hide_me, 
	'next_scrape':math.ceil(next_scrape)
	}
	return render(request,'news/home.html',context)

def scrape(request):
	user_p = UserProfile.objects.filter(user=request.user).first()#here there will be error
	#since at first user_p will be none so at first just create a userprofile
	#in the models then it will work
	user_p.last_scrape = datetime.now(timezone.utc)
	user_p.save()

	session = requests.Session()
	session.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}
	url = 'https://www.theonion.com/'

	content = session.get(url, verify=False).content

	soup =BeautifulSoup(content, 'html.parser')

	posts = soup.find_all('div',{'class':'curation-module__item'})#returns a list
	
	for i in posts:
		link = i.find_all('a',{'class':'js_curation-click'})[1]['href']
		title = i.find_all('a',{'class':'js_curation-click'})[1].text
		image_source = i.find('img',{'class':'featured-image'})['data-src']

		#stackoverflow solution
		#https://i.kinja-img.com/gawker-media/image/upload/s--AW8DYwEq--/
		#c_fill,f_auto,fl_progressive,g_center,h_264,q_80,w_470/
		#mqlrmlplwc9gxplfx5oc.jpg

		media_root = '/Users/Jukal/desktop/sites/testenv/media_root'
		if not image_source.startswith(("data:image","javascript")):
			local_filename = image_source.split('/')[-1].split("?")[0]
			r = session.get(image_source, stream=True, verify=False)
			with open(local_filename, 'wb') as f:
				for chunk in r.iter_content(chunk_size=1024):
					f.write(chunk)

			current_image_absolute_path = os.path.abspath(local_filename)
			shutil.move(current_image_absolute_path, media_root)		
        
        #end of stackoverflow

		new_headline = Headline()
		new_headline.title = title
		new_headline.url = link
		new_headline.image = local_filename
		new_headline.save()

	return redirect('/')
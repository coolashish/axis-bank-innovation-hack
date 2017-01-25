from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .forms import postQuery
import pyjarowinkler
import main

# Create your views here.


def test(request):
	if request.method == "POST" and not request.FILES:
		form = postQuery(request.POST)
		if form.is_valid():
			print form['query'].value()
                        score = processCompanyName(form['query'].value())
                        print score
                else:
                    pass
                return HttpResponse("Query Submitted, score:" + str(score))
	elif request.method == 'POST' and request.FILES['myfile']:
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
                score_list = processCompanyFile(uploaded_file_url)
		return HttpResponse("File Uploaded")
	else:
		form = postQuery()
		return render(request, "index.html", {'form' : form})

def processCompanyName(company_name):
    obj = main.Logic()
    isiec = isIEC(company_name)
    score = obj.process(company_name, isiec, settings.BASE_DIR)
    return score


def processCompanyFile(filePath):
	filePath = settings.BASE_DIR + filePath
	file = open(filePath, "r+")
        score_list = []
	for line in file:
		company = line[:len(line) - 1]
		#search.objects.create(query = company, score = 0, date = timezone.now())
                score_list.append(processCompanyName(company))
	return score_list

def isIEC(company):
        filename = settings.BASE_DIR + '/forex/iec.csv'
        f = open(filename, 'r')
        line = f.readline()
	flag = False
        while (line):
                company_name = line.split('\t')[1]
                try:
                    company_name = str(company_name)
                    company = str(company)
                    print 'Company', company
                    print 'Company name', company_name
		    dis = pyjarowinkler.get_jaro_distance(str(company), str(company_name), winkler = True, scaling = 0.1)
                except Exception as e:
                    dis = 0.7
                if(dis >= 0.85):
			flag = True
			break
                line = f.readline()
 	return flag

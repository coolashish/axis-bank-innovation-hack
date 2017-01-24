from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .forms import postQuery
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
		return HttpResponse("Query Submitted")
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
    isIEC = isIEC(company_name)
    score = obj.process(company_name, isIEC)
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
        filename = './iec.csv'
        f = open(filename, 'r')
        line = f.readline()
	flag = False
        while (line):
                company_name = line.split('\t')[1]
		dis = distance.get_jaro_distance(company, company_name, winkler = True, scaling = 0.1)
		if(dis >= 0.85):
			flag = True
			break
                line = f.readline()
 	return flag

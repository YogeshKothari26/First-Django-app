
from django.shortcuts import render, redirect
from .models import Strategy, Companies, Refreshed, Indicator, Choices,Strategy_Group
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from celery.result import AsyncResult
from .tasks import do_work
from django.http import HttpResponse
import json
import logging
import pandas as pd
import os
from django.apps import apps
import blog.extras.access_token as AT
from django.db.models import Q

logger = logging.getLogger(__name__)



def clist(request):
	Companies_List = Companies.objects.all()

	task_id = AT.get_task_id()

	result = AsyncResult(task_id)
	print('State = ' + str(result.state))

	if(not result.state == "PROGRESS"):
		task_obj = do_work.apply_async()
		task_id = task_obj.id
		print('Assigned new ID = ' + str(task_id))


	indilist=Indicator.__subclasses__()   
	Indicators_List=list()
	for a in indilist:
		a=str(a).split(".")[2]
		a=a.split("\'")[0]
		Indicators_List.append(a) 

	return render(request, 'blog/nav.html', {'companies': Companies_List,"indicatorlist":Indicators_List})



def createstrategy(request):
	if request.method == 'POST':
		if request.POST.get('indicator1') and request.POST.get('indicator2') and request.POST.get('comparator') and request.POST.get('name') and request.POST.get('instrument') :

			Strategy_Ids = list()
			inst_str = str(request.POST.get('instrument'))
			Instrument_List = list(inst_str.split(","))[:-1]

			for instruments in Instrument_List:
				strat=Strategy()             
				strat.comparator= request.POST.get('comparator')
				strat.name= request.POST.get('name')
				strat.instrument= instruments
				i1=apps.get_model("blog",request.POST.get('indicator1'))()
				i1.save()
				i2=apps.get_model("blog",request.POST.get('indicator2'))()
				i2.save()
				strat.indicator1=i1 
				strat.indicator2=i2
				strat.task_id = "task_obj.id"
				strat.save()
				Strategy_Ids.append(strat.id)
		  
			Indicator1_Fields=strat.indicator1._meta.get_fields(include_parents=False)
		
			Indicator1_Fields_Dict=dict()
			Indicator2_Fields_Dict=dict()

			for a in Indicator1_Fields:
				t=a
				a=str(a).split(".")[2]
				a=a.split("\'")[0]
				Indicator1_Fields_Dict[a]=t.default

			Indicator2_Fields=strat.indicator2._meta.get_fields(include_parents=False)
			sp2=list()

			for a in Indicator2_Fields:
				t=a
				a=str(a).split(".")[2]
				a=a.split("\'")[0]
				Indicator2_Fields_Dict[a]=t.default

			Companies_List= Companies.objects.all()  
			indilist=Indicator.__subclasses__() 
			Indicators_List=list()
			for a in indilist:
				a=str(a).split(".")[2]
				a=a.split("\'")[0]
				Indicators_List.append(a)
			choice=Choices()   
			
			Instrument_List.clear()    
			
			return render(request, "blog/nav2.html",{'companies': Companies_List,"strat":strat.id,"fieldlist1":Indicator1_Fields_Dict,"fieldlist2":Indicator2_Fields_Dict,"indicatorlist":Indicators_List,"choice":choice, "strat_obj" : strat, 
				"Strategy_Ids":str(Strategy_Ids)})
	else:
		Companies_List = Companies.objects.all()
		return render(request, "blog/nav.html",{'companies': Companies_List})  



def updatestrategy(request):
	Companies_List = Companies.objects.all()
	if request.method == 'POST':

		received = request.POST.get('Strategy_Ids')
		import ast
		Strategy_Ids = ast.literal_eval(received)

		for ids in Strategy_Ids:
			sid=ids
			strat = get_object_or_404(Strategy,pk=sid)
			strat.indicator1 = strat.indicator1.down_cast()
			strat.indicator2 = strat.indicator2.down_cast()

			Companies_List = Companies.objects.all()

			indi1=apps.get_model("blog",str(strat.indicator1.__class__.__name__))()

			indi2=apps.get_model("blog",str(strat.indicator2.__class__.__name__))()

			fullfieldlist=indi1._meta.get_fields(include_parents=False)
			shortfieldlist=list()
			i=0

			for a in fullfieldlist:
				if i==0:
					pass
				else:
					
					a=str(a).split(".")[2]
					a=a.split("\'")[0]
					shortfieldlist.append(a)
				i+=1
		   
			c=True


			for a in shortfieldlist:
				if not request.POST.get(str(a)+"1"):
					c=False

			fullfieldlist2=indi2._meta.get_fields(include_parents=False)
			shortfieldlist2=list()
			i=0

			for a in fullfieldlist2:
				if i==0:
					pass
				else:
				   
					a=str(a).split(".")[2]
					a=a.split("\'")[0]
					shortfieldlist2.append(a)
				i+=1
		  

			for a in shortfieldlist2:
				if not request.POST.get(str(a)+"2"):
					c=False



			if c:
				for a in shortfieldlist:
				   setattr(strat.indicator1,a,request.POST.get(str(a)+"1"))

				for a in shortfieldlist2:
				   setattr(strat.indicator2,a,request.POST.get(str(a)+"2"))
			
			strat.indicator1.save() 
			strat.indicator2.save()
			strat.save()
			s = Strategy.objects.all().filter(pk = strat.id)
			s = list(s)[0]
			print('Strategy created = '+str(s))

		Strategy_Ids.clear()
		r = Refreshed(name="Strategy")
		r.save()
		print("\nAdded refresh object")

		return redirect('clist') 




def display_dashboard(request):    	

	strat_list = Strategy.objects.all()

	task_id = AT.get_task_id()

	result = AsyncResult(task_id)
	print('State = ' + str(result.state))

	if(not result.state == "PROGRESS"):
		task_obj = do_work.apply_async()
		task_id = task_obj.id
		print('Assigned new ID = ' + str(task_id))


	return render(request, 'blog/dashboard.html',{"task_id" : task_id, "strat_list" : strat_list})



def revoke(request,task_id):
	strat_list = Strategy.objects.all()
	task_obj = do_work.apply_async()

	AT.set_task_id(task_obj.id)

	return redirect('/dashboard',{"task_id":task_obj.id,"strat_list":strat_list})



def get_progress(request, task_id):
	print('get_progress :: task_id :- ' + task_id)
	result = AsyncResult(task_id)
	data = dict()
	try:
		data = result.info
	except:
		print('EXCEPT')
		pass	

	return HttpResponse(json.dumps(data), content_type='application/json') 

	
			


def manage(request):
	from django.db.models import Q
	strat_list = Strategy.objects.filter(~Q(name = "DO_NOT_DELETE"))

	strat_group = Strategy_Group.objects.filter(~Q(name = "DO_NOT_DELETE"))

	return render(request, 'blog/manage.html',{"strat_list":strat_list, "strat_group_list":strat_group})

def strat_detail(request,pk):
	strat = get_object_or_404(Strategy,pk=pk)

	strat.indicator1.delete()
	strat.indicator2.delete()
	strat.delete()
	
	r = Refreshed(name="Strategy")
	r.save()
	print("\nAdded refresh object")
	return redirect('manage')

def strat_group_detail(request,pk):
	strat = get_object_or_404(Strategy,pk=pk)
	strat.delete()
	
	r = Refreshed(name="Strategy_Group")
	r.save()
	print("\nAdded refresh object")
	return redirect('manage')


def delete_all(request):	

	for strat in Strategy.objects.filter(~Q(name = "DO_NOT_DELETE")):
		try:
			strat.indicator1.delete()
			strat.indicator2.delete()
			strat.delete()
		except:
			strat.delete()

	for strat in Strategy_Group.objects.filter(~Q(name = "DO_NOT_DELETE")):
		strat.delete()

	r = Refreshed(name="Strategy")
	r.save()
	r = Refreshed(name="Strategy_Group")
	r.save()
	print("\nAdded refresh object")
	return redirect('manage')



def stratgroup(request):

	global Strategy_Ids
	Strategy_Ids.clear()

	strat_list = Strategy.objects.filter(~Q(name = "DO_NOT_DELETE"))


	return render(request, 'blog/stratgroup.html',{"strat_list":strat_list})


def stratgroupsubmit(request):
	
	Companies_List = Companies.objects.all() 

	if request.method == 'POST':

		group=Strategy_Group()
		group.name=request.POST.get('groupname')
		group.exp=request.POST.get('groupid') 
		group.display = request.POST.get('groupstring')
		group.save()

		print("Group created with "+ group.name+"   "+group.exp)

		r = Refreshed(name="Strategy_Group")
		r.save()

	return render(request, "blog/nav.html",{'companies': Companies_List})  














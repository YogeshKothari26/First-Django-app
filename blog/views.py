
from django.shortcuts import render, redirect
from .models import Strategy, Companies, Refreshed, Indicator, Choices,Strategy_Group, Watch_List
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
from .user_functions import *
from django.db.models import Q
import django.contrib.auth as auth

logger = logging.getLogger(__name__)
# To- Do
# Dropdown clear


def login(request):
	return render(request, 'blog/login.html', {})


def error(request):
	return render(request, 'blog/error.html', {})


def login_submit(request):
	print('submitted')
	if request.method == 'GET':
		return render(request, 'blog/login.html')

	if request.method == 'POST':
		username = request.POST.get('uname', '')
		# username = request.POST.get('email', '')
		password = request.POST.get('psw', '')

		user = auth.authenticate(username=username, password=password)
		if user is None:
			print('None')
			return redirect('error')
		if not user.is_active:
			print('not active')
			return redirect('error')

		# Correct password, and the user is marked "active"
		auth.login(request, user)
		# Redirect to a success page.
		print('success!')
		return redirect('clist')


def clist(request):
	print(type(request.user))
	print(request.user.pk)
	print(request.user)	
	print('\n\n' + str(request.user.__dict__))

	slist = Strategy.objects.filter(added_by=request.user)	
	print('strat list :' +str(slist))
	slist = Strategy_Group.objects.filter(added_by=request.user)	
	print('strat group list :' +str(slist))

	Companies_List = Companies.objects.all()
	watchlist = Watch_List.objects.all()
	
	for w in watchlist:
		w.company_list =  w.company_list[1:-1]

	task_id = get_task_id(request.user.pk)

	result = AsyncResult(task_id)
	print('State = ' + str(result.state))

	if(not result.state == "PROGRESS"):
		task_obj = do_work.delay(user_pk=request.user.pk)
		task_id = task_obj.id
		print('Assigned new ID = ' + str(task_id))


	indilist=Indicator.__subclasses__()   
	Indicators_List=list()
	for a in indilist:
		a=str(a).split(".")[2]
		a=a.split("\'")[0]
		Indicators_List.append(a) 

	return render(request, 'blog/homepage3.html', {'companies': Companies_List,"indicatorlist":Indicators_List, 
		"watchlist" : watchlist})




def manage(request):
	print(request.user)
	strat_list = list(Strategy_Group.objects.all())
	w_list = list(Watch_List.objects.all())

	return render(request, 'blog/manage2.html', {"strat_list": strat_list, 'w_list':w_list})




def display_dashboard(request):     

	strat_list = Strategy.objects.all() 

	task_id = get_task_id(request.user.pk)

	result = AsyncResult(task_id)
	print('State = ' + str(result.state))
	print('task_id = '+str(task_id))

	if(not result.state == "PROGRESS"):
		task_obj = do_work.delay(user_pk=request.user.pk)
		task_id = task_obj.id
		print('Assigned new ID = ' + str(task_id))


	return render(request, 'blog/dashboard.html',{"task_id" : task_id, "strat_list" : strat_list})



def revoke(request,task_id):
	strat_list = Strategy.objects.all()
	task_obj = do_work.delay(user_pk=request.user.pk)

	set_task_id(request.user.pk, task_obj.id)

	return redirect('/dashboard',{"task_id":task_obj.id,"strat_list":strat_list})




def get_progress(request, task_id):
	print('get_progress :: task_id :- ' + task_id)
	result = AsyncResult(task_id)
	data = dict()
	try:
		data = result.info
		# print('\n####Data : ' + str(data))
	except:
		# print('Error RESULT \n state = ' + str(result.state) + '\tDetails = '+str(result.info))
		print('EXCEPT')
		pass    

	return HttpResponse(json.dumps(data), content_type='application/json')  



def delete_strategy(pk):
	print('delete_strategy :'+str(pk))
	strat = get_object_or_404(Strategy,pk=pk)

	strat.indicator1.delete()
	strat.indicator2.delete()
	strat.delete()	


def delete_strat_group(request,pk):
	print('delete_strat_group :'+str(pk))
	sg = get_object_or_404(Strategy_Group,pk=pk)
	l = sg.exp.split(' ')
	
	print('split = '+str(l))
	for i in l:
		if(i not in ['and', 'or', 'not', 'True', 'False']):
			try:
				delete_strategy(int(i))
			except:
				print('except -> strategy :'+i)

	sg.delete()
	
	set_refresh(request.user.pk, True)
	print("\nAdded refresh object")
	return redirect('manage')


def delete_watchlist(request,pk):
	print('delete_watchlist :'+str(pk))
	w = get_object_or_404(Watch_List,pk=pk)
	w.delete()
	
	return redirect('manage')       


def delete_all(request):    
	print('delete_all')

	# for strat in Strategy.objects.filter(~Q(name = "DO_NOT_DELETE")):
	for strat in Strategy.objects.all():
		try:
			strat.indicator1.delete()
			strat.indicator2.delete()
			strat.delete()
		except:
			strat.delete()

	# for strat in Strategy_Group.objects.filter(~Q(name = "DO_NOT_DELETE")):
	for strat in Strategy_Group.objects.all():
		strat.delete()

	set_refresh(request.user.pk, True)
	print("\nAdded refresh object")
	return redirect('manage')



def delete_extra_indicators():
	slist = Strategy.objects.all()
	ilist = [s.indicator1 for s in slist]		
	ilist = ilist + [s.indicator2 for s in slist]	#used indicators
	ilist = list(set(ilist))
	
	for i in Indicator.objects.all():
		if i not in ilist:
			print('deleting : '+str(i))
			i.delete()



def indicator_popup(request, selected_indicator):
	print('\nindicator_popup')
	data = dict()
	try:
		fields = dict()
		i = apps.get_model("blog",selected_indicator)
		print('i = '+str(i))    
		for f in i._meta.get_fields(include_parents=False)[1:]:
			fields[str(f).split(".")[2]] = f.default
		choice=Choices()
		data = {'fields' : fields, 'choice':choice.__dict__}

		print(data)

	except:
		pass

	return HttpResponse(json.dumps(data), content_type='application/json') 



def watchlist(request):
	Companies_List = Companies.objects.all()

	return render(request, 'blog/watchlist.html', {'companies': Companies_List})

def submit_watchlist(request):
	if request.method == 'POST':
		if request.POST.get('instrument') and request.POST.get('wlist_name'):
			inst_str = "["+ str(request.POST.get('instrument')) +"]"
			w = Watch_List()
			w.name = request.POST.get('wlist_name')
			w.company_list = inst_str
			w.save()
			print("Done")
			print("Instruments Are: "+inst_str+ ","+w.name+","+ w.company_list)
	return redirect('watchlist')


def create_indicator(request):
	print("view : create_indicator")

	if request.method == 'POST':
		
		if request.POST.get('selected_indicator'):          
			selected_indicator = request.POST.get('selected_indicator')
			i = apps.get_model("blog",selected_indicator)() 
			model_name=type(i)
			print(model_name.__name__)      
		

			fields  = [str(f).split(".")[2]   for f in i._meta.get_fields(include_parents=False)[1:]  ]
			print('fields = '+str(fields))

			for f in fields:
				setattr(i, f, request.POST.get(f))
			i.save()

			print('i  = '+str(i))

		data = {'pk' : i.pk, 'name' : str(i),'model':str(model_name.__name__)}          
						
	return HttpResponse(json.dumps(data), content_type='application/json') 




def form_sub(request):
	Temporary_Strategy_Ids=list()
	list_of_list=list()
	import ast
	comparator_dict=dict()
	comparator_dict= {
			"GreaterThan":"1",
			"LessThan":"2",
			"CrossesAbove":"3",
			"CrossesBelow":"4"
	}

	sg_display = ""
	if request.method == 'POST':

		no_of_strat=request.POST.get('no_of_strat')

		received_tokens = request.POST.get('token_list')        
		tokens = list(set(ast.literal_eval(received_tokens)))

		for i in range(1,int(no_of_strat)+1):
			print("i is"+str(i))
			Temporary_Strategy_Ids.clear()
			for j in tokens:
				Full_Name=request.POST.get('strategy_indicator_name-'+str(i)+"1")
				className1=apps.get_model("blog",Full_Name)

				Full_Name=request.POST.get('strategy_indicator_name-'+str(i)+"3")
				className3=apps.get_model("blog",Full_Name)
		
			
				strat=Strategy()  
					 
				strat.comparator= comparator_dict[request.POST.get('strategy_part-'+str(i)+"2")]
				print(strat.comparator)

				strat.name= str(i)+":"+request.POST.get('group_name')+"("+str(j)+")"
				strat.instrument= str(j)  
				strat.added_by = request.user              
				
				i1 = get_object_or_404(className1,pk=request.POST.get('strategy_part-'+str(i)+"1"))
				i2 = get_object_or_404(className3,pk=request.POST.get('strategy_part-'+str(i)+"3"))

				# For cloning of objects
				
				i1.pk=None
				i2.pk=None
				i1.id=None
				i2.id=None
				i1.save()
				i2.save()
				strat.indicator1=i1

				strat.indicator2=i2
				print(strat.indicator1)
				print(strat.indicator2)
				print('strat user = '+str(strat.added_by))
				strat.task_id = "task_obj.id"
				strat.save()

				print("saved")
				Temporary_Strategy_Ids.append(strat.id)
				print(str(strat.id)+" "+str(Temporary_Strategy_Ids))
				print("list is "+str(list_of_list))



			list_of_list.append(Temporary_Strategy_Ids.copy())
			print("here")


		print(str(list_of_list))		

		# For strategy groups

		for index1, val_token in enumerate(tokens):
			group_id_string=str()
			group_name_string=str()
			group_name=request.POST.get('group_name')

			for index2 in range(int(no_of_strat)):
				if(group_id_string == ""):
					group_id_string=str(list_of_list[index2][index1])

				else:
					group_id_string=str(group_id_string)+" "+str(list_of_list[index2][index1])

				i1 = get_object_or_404(Strategy,pk=list_of_list[index2][index1])
				group_name_string=str(group_name_string)+" "+str(i1)
				# sg_display = sg_display + 
				if(index2!=(int(no_of_strat)-1)):
					cond = str(request.POST.get('strategy_condition-'+str(index2+1)))
					group_id_string=str(group_id_string)+" "+ cond
					group_name_string=str(group_name_string)+" "+cond



			group=Strategy_Group()
			group.name=request.POST.get('group_name')+":"+str(val_token)
			group.exp=group_id_string 
			group.display =group_name_string
			group.entry_condition=request.POST.get('entry_condition')        
			comp_name = Companies.objects.filter(token = val_token)
			group.comp_name = str(list(comp_name)[0].name)
			group.added_by = request.user
			group.save()

			print('group user = '+str(group.added_by))
			set_refresh(request.user.pk, True)
			print("\nAdded refresh object")

			print("Group created with "+ str(group.name)+"   "+str(group.exp))

		

		# Clearing out extra strategies

		received_studies=request.POST.get('study_list')
		studies=ast.literal_eval(received_studies)

	return redirect('clist')










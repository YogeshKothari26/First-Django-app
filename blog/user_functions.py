from django.contrib.auth.models import User
from blog.models import User_Data
from django.shortcuts import get_object_or_404

def get_user_data(user_pk):
	user = get_object_or_404(User,pk=user_pk)
	user_data = User_Data.objects.filter(user_fkey = user)
	return list(user_data)[0]

def set_access_token(user_pk, access_token):
	user_data = get_user_data(user_pk)	
	user_data.access_token = access_token

def get_access_token(user_pk):
	user_data = get_user_data(user_pk)
	return user_data.access_token	

def set_all_access_token(access_token):		#same value for all user
	qs = User_Data.objects.all()
	qs.update(access_token=access_token)

def set_task_id(user_pk, task_id):
	user_data = get_user_data(user_pk)
	user_data.task_id = task_id
	user_data.save()

def get_task_id(user_pk):
	user_data = get_user_data(user_pk)
	return user_data.task_id


def set_refresh(user_pk, value):
	user_data = get_user_data(user_pk)
	user_data.refresh = str(value)	#str(True/False)
	user_data.save()

def get_refresh(user_pk):
	user_data = get_user_data(user_pk)
	return user_data.refresh == 'True'
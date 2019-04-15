
from selenium import webdriver
from kiteconnect import KiteConnect
from time import sleep
from apscheduler.schedulers.blocking import BlockingScheduler
import pandas as pd
import datetime
import os
from blog import user_functions as UF
import pandas as pd


def kite_login():
	print('Login Time : ' + str(pd.Timestamp('today')))

	flag = True
	print('cwd : '+str(os.getcwd()))
	browser = webdriver.PhantomJS(executable_path= os.getcwd() + r"\blog\extras\phantomjs-2.1.1-windows\bin\phantomjs")
	while flag:
		try:		
			# insert page link
			browser.get("https://kite.trade/connect/login?api_key=0ld4qxtvnif715ls&v=3")
			sleep(2)
			count = 0
			# insert credential
			username = browser.find_element_by_css_selector("input[type='text']")
			username.send_keys('ZB8746')
			password = browser.find_element_by_css_selector("input[type='password']")
			password.send_keys('@KKR357')
			browser.find_element_by_css_selector("button[type='submit']").click()

			print('Username: ZB8746')
			print('Password: @KKR357')
			sleep(5)


			question1 = browser.find_elements_by_css_selector("input")[0]
			question1.send_keys('050991')
			browser.find_element_by_css_selector("button[type='submit']").click()
			sleep(5)   

			s = browser.current_url
			for i in range(10):
				try:
					request_token = (s.split('request_token='))[1].split('&action')[0]
					break
				except:
					count += 1
					print('try: ', count)
					sleep(2)
					pass

			kite = KiteConnect(api_key="0ld4qxtvnif715ls")
			api_key="0ld4qxtvnif715ls"
			api_secret="1lg2kjkba3ol83aospgrovvqd5uvetyn"
			kite=KiteConnect(api_key,api_secret)
			dic = kite.generate_session(request_token, api_secret)

			print('access token = ' +str(dic['access_token']))
			UF.set_all_access_token(str(dic['access_token']))
			return
		except:
			print("ERROR KITE LOGIN")
			return
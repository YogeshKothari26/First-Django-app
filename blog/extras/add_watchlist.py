from blog.models import Companies, Watch_List
import pandas as pd
# import ast


clist = Companies.objects.all()
df = pd.read_csv('nifty50list.csv')
symbols = list(df['Symbol'])

w = Watch_List()
w.name = 'Nifty 50'
nifty = clist.filter(name__in = symbols)
w.company_list = str([n.pk for n in nifty])
w.save()

#use ast.eval_literal(str_list) to get list of int tokens


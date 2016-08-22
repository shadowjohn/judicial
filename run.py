# -*- coding: utf-8 -*-
import sys
import re
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
import include
import function
#from bs4 import BeautifulSoup
my = include.kit();
myf = function.kit();
#print(my.date("Y-m-d"));
# Get gov lists
gov_lists = myf.get_gov_list(my);
print(gov_lists)

for item in gov_lists:
  #http://aomp.judicial.gov.tw/abbs/wkw/WHD2A02.jsp?proptype=C52&saletype=1&court=TPD
  #http://www.judicial.gov.tw/db/alx.asp
  #房屋+一般程序=http://aomp.judicial.gov.tw/abbs/wkw/WHD2A02.jsp?proptype=C52&saletype=1&court=TPD
  #<input type="hidden" name="5895C58FCBA07BFB795B873628D67BE6" value="6327D09D511F1F5E4A84C13E9275CBAC">
  key_obj = myf.get_secret_key(my,item);
  #print(key_obj);
  
  
  myf.get_page_lists(my,item,key_obj);
  my.exit();
  ##http://aomp.judicial.gov.tw/abbs/wkw/WHD2A03.jsp?5895C58FCBA07BFB795B873628D67BE6=6327D09D511F1F5E4A84C13E9275CBAC&hsimun=all&ctmd=all&sec=all&saledate1=&saledate2=&crmyy=&crmid=&crmno=&dpt=&minprice1=&minprice2=&saleno=&area1=&area2=&registeno=&checkyn=all&emptyyn=all&rrange=%A4%A3%A4%C0&comm_yn=&owner1=&order=odcrm&courtX=TPD&proptypeX=C52&saletypeX=1&query_typeX=db
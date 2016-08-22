# -*- coding: utf-8 -*-
import re
import math
from bs4 import BeautifulSoup
# C52 = 房屋、一般程序
class kit: 
  def get_gov_list(self,my): 
    data = my.file_get_contents_post("http://aomp.judicial.gov.tw/abbs/wkw/WHD2A00.jsp","");    
    sdata = str(data, 'Big5',"ignore");    
    s = my.get_between(sdata,"<select name=\"court\" size=\"1\">","</select>");
    s = my.trim(s);
    s = my.str_replace("\r","",s);
    s = my.str_replace("\t","",s);
    gov_list = [];
    m = my.explode("\n",s);
    for item in m:
      # <option value="ILD">臺灣宜蘭地方法院</option>',
      d = {};
      item = my.trim(item);
      m = re.search('<option value="(.*)">(.*)</option>',item);
      d['key']=m.group(1);
      d['name']=m.group(2);
      my.array_push(gov_list,d)
    #print(gov_list);
    return gov_list;
  def get_secret_key(self,my,item):
    key = "";
    URL = "http://aomp.judicial.gov.tw/abbs/wkw/WHD2A02.jsp?proptype=C52&saletype=1";
    URL+="&court="+item["key"];
    data = my.file_get_contents_post(URL,"")
    sdata = str(data, 'Big5',"ignore");
    #<input type="hidden" name="5895C58FCBA07BFB795B873628D67BE6" value="6327D09D511F1F5E4A84C13E9275CBAC">
    k = re.search("<input type=\"hidden\" name=\"(.*)\" value=\"(.*)\">",sdata);
    #print(k.group(1)+","+k.group(2));
    key_obj = {};
    key_obj[k.group(1)]=k.group(2);
    return key_obj;
  def get_page_lists(self,my,item,key_obj):
    URL="http://aomp.judicial.gov.tw/abbs/wkw/WHD2A03.jsp?";
    #URL+="5895C58FCBA07BFB795B873628D67BE6=6327D09D511F1F5E4A84C13E9275CBAC"
    key = list(key_obj.keys())[0];
    URL+=key+"="+key_obj[key];       
    URL+="&hsimun=all&ctmd=all&sec=all&saledate1=";
    URL+="&saledate2=&crmyy=&crmid=&crmno=&dpt=&minprice1=";
    URL+="&minprice2=&saleno=&area1=&area2=&registeno=";
    URL+="&checkyn=all&emptyyn=all&rrange=%A4%A3%A4%C0";
    URL+="&comm_yn=&owner1=&order=odcrm";
    URL+="&courtX="+item["key"];
    URL+="&proptypeX=C52";
    URL+="&saletypeX=1&query_typeX=db";
    data = my.file_get_contents_post(URL,"")
    sdata = str(data, 'Big5',"ignore");
    
    #每頁15筆
    #合計件數: 155 件   
    find_total = re.search("合計件數:&nbsp;(.*)&nbsp;件",sdata);
    totals=int(my.trim(find_total.group(1)))
    total_pages = my.ceil(totals/15);
    #print(total_pages)
    #my.exit();
    #POSTS_STRING=URL;

    for i in range(1,total_pages+1):
      POSTS_STRING="";
      POSTS_STRING+="pageTotal="+str(total_pages);
      POSTS_STRING+="&pageSize=15";    
      POSTS_STRING+="&rowStart=1&saletypeX=1&proptypeX=C52";    
      POSTS_STRING+="&courtX="+item["key"];
      POSTS_STRING+="&order=odcrm";
      POSTS_STRING+="&query_typeX=session&saleno=";
      POSTS_STRING+="&hsimun=all&ctmd=all&sec=all";
      POSTS_STRING+="&crmyy=&crmid=&crmno=&dpt=";
      POSTS_STRING+="&saledate1=&saledate2=&minprice1=";
      POSTS_STRING+="&minprice2=&sumprice1=&sumprice2=";
      POSTS_STRING+="&area1=&area2=&r";    
      POSTS_STRING+="&pageNow="+str(i);
      page_data = my.file_get_contents_post(URL,POSTS_STRING);
      spage_data = str(page_data, 'Big5',"ignore");
      soup = BeautifulSoup(spage_data,'html.parser');
      for link in soup.find_all("tr"):
        slink = str(link);
        if my.is_string_like(slink,"<a href=\"WHD2ASHOW.jsp?rowid="):
          #slink = my.str_replace("\n","",slink);
          #slink = my.str_replace(" ","",slink);
          slink = my.trim(slink);
          #print(slink+"\n");
          slink_soup = BeautifulSoup(slink,'html.parser');
          #筆次
          ID = my.trim(slink_soup.div.get_text());
          if my.is_numeric(ID) == False:
            continue;
          #藍地址
          STRING = my.trim(slink_soup.a.get_text());
          #連結 
          LINK = "http://aomp.judicial.gov.tw/abbs/wkw/" + slink_soup.a.get("href");           
          print( ID + " : " + STRING + " : " + LINK + "\n\n");
          filename = ID+"_"+STRING+".txt";
          
          #已存在就跳過
          if my.is_file("DOWNLOAD\\"+filename):
            continue;
          
          #接下來是取得內頁的內容
          URL = LINK;
          contents = my.file_get_contents_post(URL,"");
          scontents_data = str(contents, 'Big5',"ignore");
          cut_spage_data = my.get_between(scontents_data,"~","~");
          my.file_put_contents("DOWNLOAD\\"+filename,my.s2b(cut_spage_data));  
      #my.exit();
      #cut_spage_data = my.get_between(spage_data,"~","~");
      #my.file_put_contents("tmp\\"+str(i)+".htm",my.s2b(cut_spage_data));  
    my.exit();
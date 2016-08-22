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

txts = my.glob("DOWNLOAD\\*.txt");
#step=1
for filename in txts:
  print(filename);
      
  mn = my.mainname(filename);
  dn = my.dirname(filename);
  data = my.file_get_contents(filename);
  data = my.str_replace("\r","",data);
  mdata = my.explode("\n",data);
  OUTPUT = {};
  OUTPUT["主條目"] = {};
  OUTPUT["主條目"]["content"]=[];
  #得收到content了
  #OUTPUT["主條目"]["編號"]={};
  #OUTPUT["主條目"]["土地坐落"]={};
  #OUTPUT["主條目"]["土地坐落"]["縣市"]="";
  #OUTPUT["主條目"]["土地坐落"]["鄉鎮市區"]="";
  #OUTPUT["主條目"]["土地坐落"]["段"]="";
  #OUTPUT["主條目"]["土地坐落"]["小段"]="";
  #OUTPUT["主條目"]["土地坐落"]["地號"]="";
  #OUTPUT["主條目"]["地目"]="";
  #OUTPUT["主條目"]["面積平方公尺"]="";
  #OUTPUT["主條目"]["權利範圍"]="";
  #OUTPUT["主條目"]["最低拍賣價格"]="";  
  OUTPUT["細條目"] = {};
  OUTPUT["細條目"]["content"] = [];
  OUTPUT["細條目"]["點交情形"] = "";
  OUTPUT["細條目"]["使用情形"] = "";
  OUTPUT["細條目"]["備註"] = "";
  
  #開始爬
  sdata = my.get_between(data,"│號│縣　市│鄉鎮市區│　段　│小段  │  地　　號  │目","└─┴───┴───────────────────────────────────────────┘");
  sdata = my.str_replace("├─┼───┼────┼───┼───┼──────┼─┼─────┼──────┼────────┤","",sdata);
  sdata = my.trim(sdata);
  msdata = my.explode("├─┼───┼────┬───┬───┬──────┬─┬─────┬──────┬────────┤",sdata);
  for item in msdata:
    d = {};
    mitem = my.explode("│  ├───┼────┴───┴───┴──────┴─┴─────┴──────┴────────┤",item);
    #mitem[0] = 主條目內容
    #mitem[1] = 備考
    #print(mitem[1]);
    m = re.search("│(.*)│(.*)│(.*)│(.*)│(.*)│(.*)│(.*)│(.*)│(.*)│(.*)│",mitem[0]);
    print(m);
    if m == None: 
      continue;
    d["土地坐落"]={};
    d["土地坐落"]["編號"]=my.trim(m.group(1));
    d["土地坐落"]["縣市"]=my.trim(m.group(2));
    d["土地坐落"]["鄉鎮市區"]=my.trim(m.group(3));
    d["土地坐落"]["段"]=my.trim(m.group(4));
    d["土地坐落"]["小段"]=my.trim(m.group(5));
    d["土地坐落"]["地號"]=my.trim(m.group(6));
    d["地目"]=my.trim(m.group(7));
    d["面積平方公尺"]=my.trim(m.group(8));
    d["權利範圍"]=my.trim(m.group(9));
    d["最低拍賣價格"]=my.trim(m.group(10));
    m = re.search("│(.*)│備考  │(.*)│",mitem[1]);
    d["備考"]=my.trim(m.group(2));
    my.array_push(OUTPUT["主條目"]["content"],d);      
  #####################################
  #######  這區是爬細目條的   #########
  #####################################
  sdata = my.get_between(data,"│號│    │              │屋層數│合　　　　　　　　計","│點交情形│");
  sdata = my.str_replace("  │及用途    │  範圍  │                  │","",sdata);
  sdata = my.str_replace("├─┼──┼───────┼───┼───────────┼─────┼────┼─────────┤","",sdata);
  sdata = my.str_replace("├─┴──┼────────────────────────────────────────────┤","",sdata);  
  sdata = my.trim(sdata);
  msdata = my.explode("├─┼──┼───────┬───┬───────────┬─────┬────┬─────────┤",sdata);
  #print(sdata);
  #my.exit();
  for item in msdata:
    item = my.trim(item);
    #print(item);
    #print("\n\n\n");
    d = {};
    mitem = my.explode("│  ├──┼───────┴───┴───────────┴─────┴────┴─────────┤",item);
    mitem[0] = my.trim(mitem[0]);
    mitem[1] = my.trim(mitem[1]);
    #mitem[0] = 細條目內容
    #mitem[1] = 備考
    #細條目內容為多行
    '''
    "建號": 975,
    "基地坐落": "台北市萬華區福星段512地號",
    "建物門牌": "台北市萬華區和沒接28之12號",
    "建築式樣主要建築材料": "鋼筋混凝土造",
    "房屋層數": "6層樓",
    "建物面積": {
      "樓層面積": "一層:6.74",
      "合計": "合計:6.74",
      "附屬建物主要建築材料及用途": null
    },
    "權利範圍": "2922/10000",
    "最低拍賣價格": 16000,
    "備考": "含共同使用部分964建號之持分"
    '''
    d["建號"]="";
    d["基地坐落"]="";
    d["建物門牌"]="";
    d["建築式樣主要建築材料"]="";
    d["房屋層數"]="";
    d["建物面積"]={};
    d["建物面積"]["樓層面積"]={};
    d["建物面積"]["樓層面積"]["樓層面積"]="";
    d["建物面積"]["樓層面積"]["合計"]="";
    d["建物面積"]["樓層面積"]["附屬建物主要建築材料及用途"]="";
    d["權利範圍"]="";
    d["最低拍賣價格"]="";
    d["備考"]="";
    mmitem=my.explode("\n",mitem[0]);
    for item_line in mmitem:
      m = re.search("│(.*)│(.*)│(.*)│(.*)│(.*)│(.*)│(.*)│(.*)│",item_line);
      if m == None: 
        continue;
      d["建號"]+=my.trim(m.group(2));
      d["基地坐落"]+=my.trim(m.group(3));
      d["建物門牌"]=""; #最後要再切-------
      d["建築式樣主要建築材料"]+=my.trim(m.group(3));
      d["房屋層數"]+=my.trim(m.group(4));
      d["建物面積"]["樓層面積"]["樓層面積"]+=my.trim(m.group(5));
      d["建物面積"]["樓層面積"]["合計"]=""; #最後要再切合計的部分
      d["建物面積"]["樓層面積"]["附屬建物主要建築材料及用途"]+=my.trim(m.group(6));
      d["權利範圍"]+=my.trim(m.group(7));
      d["最低拍賣價格"]+=my.trim(m.group(8));
    mmitem=my.explode("\n",mitem[1]);    
    for item_line in mmitem:            
      m = re.search("│(.*)│(.*)│(.*)│",item_line);
      print(m)
      if m == None: 
        continue;      
      d["備考"]+=my.trim(m.group(3));
    m=my.explode("--------------",d["基地坐落"]);
    d["基地坐落"]=my.trim(m[0]);
    d["建物門牌"]=my.trim(m[1]);
    
    d["建物面積"]["樓層面積"]["樓層面積"]=my.str_replace(" ","",d["建物面積"]["樓層面積"]["樓層面積"]);
    m=my.explode("合計：",d["建物面積"]["樓層面積"]["樓層面積"]);
    d["建物面積"]["樓層面積"]["樓層面積"]=my.trim(m[0]);
    d["建物面積"]["樓層面積"]["合計"]=my.trim(m[1]);  
    my.array_push(OUTPUT["細條目"]["content"],d);
  
  
  
         
  #細條目-點交情形  
  OUTPUT["細條目"]["點交情形"]="";
  check=True;
  for i in range(1,len(mdata)):
    if check == False:
      break;
    if my.is_string_like(mdata[i],"│點交情形│"):
      for j in range(i,len(mdata)):
        if my.is_string_like(mdata[j],"───────"):
          check=False;
          break;
        else:
          LD = mdata[j][5:100];          
          LD = my.trim(my.get_between(LD,"│","│"));
          OUTPUT["細條目"]["點交情形"] += LD;          
      break; 
  #細條目-使用情形
  OUTPUT["細條目"]["使用情形"]="";
  check=True;
  for i in range(1,len(mdata)):
    if check == False:
      break;
    if my.is_string_like(mdata[i],"│使用情形│"):
      for j in range(i,len(mdata)):
        if my.is_string_like(mdata[j],"───────"):
          check=False;
          break;
        else:
          LD = mdata[j][5:100];          
          LD = my.trim(my.get_between(LD,"│","│"));
          OUTPUT["細條目"]["使用情形"] += LD + "\n";          
      break;
  #細條目-備註  
  OUTPUT["細條目"]["備註"]="";
  check=True;
  for i in range(1,len(mdata)):
    if check == False:
      break;
    if my.is_string_like(mdata[i],"│備註    │"):
      for j in range(i,len(mdata)):
        if my.is_string_like(mdata[j],"───────"):
          check=False;
          break;
        else:
          LD = mdata[j][5:100];          
          LD = my.trim(my.get_between(LD,"│","│"));
          OUTPUT["細條目"]["備註"] += LD + "\n";          
      break;   
  print(OUTPUT["細條目"]["點交情形"]);
  print(OUTPUT["細條目"]["使用情形"]);
  print(OUTPUT["細條目"]["備註"]);
  
  #OUTPUT["SOURCE"]=data;
  jOUTPUT = my.json_encode_utf8(OUTPUT);
  jFOUTPUT = my.json_format_utf8(jOUTPUT);
  #print(my.json_format(jOUTPUT));
  OUTPUT_FILENAME=mn+".json";
  my.file_put_contents(OUTPUT_FILENAME,my.s2b(jFOUTPUT));
  print(mn);
  print(dn);
  #my.exit();
  
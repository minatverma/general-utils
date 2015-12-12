import csv
import sys
import os

def main():

  fprint( "\n\nEnter number corresponding to the operation you want to perform")
  fprint( "_"*70)
  fprint( "\n\t1 - Check distinct Values" )
  fprint( "\t2 - Validate File" ) 
  fprint( "\t3 - Re-order File Columns" ) 
  fprint( "\t4 - Exit" )
  try:
    option = int(raw_input())
    if option == 1 :
      checkDistinctValues()
    elif option == 2 :
      validateFile()
    elif option == 3 :
      ReorderFile()
    elif option == 4 :
      exit_program()
  except  :
    e = sys.exc_info()


def file_type():

  variables()
  fprint( "\nWhich file you want to validate . Enter corresponding number .\n ")
  
  for index, value in enumerate(variables.files) :
    fprint ('\t' + str(index+1)  + '.\t' + value[1])
  while True:
    try:
      option = int(raw_input())
      fprint(option)
      if option > len(variables.files) or option < 1 :
        fprint('Option Should be between 1 and ' + str(len(variables.files)))
        continue
    except ValueError:
      fprint('Option Should be between 1 and ' + str(len(variables.files)))
    else:
      break
  return option


def validateFile():
  option = file_type()
  file, DataCaptured = open_file()
  validateDelimiter(option,file, DataCaptured)
  validateHeader(option,file, DataCaptured)
  validateData(option,file, DataCaptured)

  close_file(file)
  main()

def ReorderFile():
  file, DataCaptured = open_file()
  headerString = next(DataCaptured)
  headerDict = {}
  key = 0
  fprint( "\nBelow are the columns present in the file :\n" )
  for header in headerString :
    key = key + 1
    headerDict [key] = header
  fprint( 'Index\t\tHeader' )
  fprint( '_'*8+'\t'+'_'*8 )
  for key in headerDict:
    fprint( str(key) +'\t:\t' + headerDict [key] ) 
  fprint('\nEnter the new order comma separated number\n')
  new_order_array = map(int,list(raw_input().strip(' ').strip('\n').split(',')))
  old_order = range(key)
  old_order = [i+1 for i in old_order]
  difference_order_1 = list(set(new_order_array) - set(old_order))
  difference_order_2 = list(set(old_order) -set( new_order_array))
  if difference_order_1:
    fprint("\nPlease review new column order")
    fprint("\n\tIt consist of new numbers \t" + str(difference_order_1) )
  if difference_order_2:
    fprint("\t\tMissing numbers \t" + str(difference_order_2) )
  if len(set(new_order_array)) == len(set(old_order)) and len(new_order_array) == len(old_order):
    fprint ("\nEverything okay. Proceeding with column re-order. Please wait a while ...")
    file.seek(0)
    if ',' in file.readline():
      delim = ','
    elif ';' in file.readline():
      delim = ';'
    file.seek(0)
    try:
      with open('out.csv', 'w') as a, file as b:
        for line in b:
          row = line.strip('\n').split(delim)
          a.writelines(delim.join([row[i-1] for i in new_order_array])+'\n')
    except IOError as e:
      print 'Operation failed: %s' % e.strerror
  else :
    fprint("\nCheck the new column order once again")
  close_file(file)
  fprint("\n\nRe-ordering of columns done. Name of file is 'out.csv' in current path.\n")


def validateDelimiter(option,file, DataCaptured):
  variables()
  siaDelimiter = variables.delimiter_map[variables.files[option - 1][0]]
  fprint( "\nChecking Delimiter.." )
  fprint( "_"*20 )
  file.seek(0)
  if ',' in file.readline():
    delim = ','
  elif ';' in file.readline():
    delim = ';'
  if siaDelimiter == delim :
    fprint( "\n\tSUCCESS" )
  else:
    fprint( "Delimiter of files are not proper" )
    fprint( "\n\tExpected = " + siaDelimiter )
    fprint( "\tGot  = " + delim )

def validateHeader(option,file, DataCaptured):
  variables()
  siaHeader = variables.headerList[variables.files[option - 1][0]]
  file.seek(0)
  if ',' in file.readline():
    delim = ','
  elif ';' in file.readline():
    delim = ';'
  file.seek(0)
  header = list()
  for a in file.readline().split(delim):
    header.append(a.strip().strip('"').strip("'"))
  fprint( "\nChecking Header.." )
  fprint( "_"*20 )
  if siaHeader == header:
    fprint( "\n\tSUCCESS" )
  else:
    fprint( "\n\tHeaders are not in proper order" )
    fprint( "\n\tExpected : " + ', '.join(siaHeader))
    fprint( "\n\tGot      : " + ', '.join(header))
  return header

def getHeaderName(option,dimension) :
  variables()
  dim = variables.headername[variables.files[option - 1][0]][dimension][1]
  return dim

def validateData(option,file, DataCaptured):
  variables()
  numberOfFiles = variables.headername[variables.files[option - 1][0]]
  for i in xrange(len(numberOfFiles)):
    currentDimension = variables.headername[variables.files[option - 1][0]][i][0]
    variableMap = currentDimension.lower() + '_map'
    siaVals = getattr(variables, variableMap)[variables.files[option - 1][0]]
    distinctDim = set()
    file.seek(0)
    dictKey = variables.files[option - 1][0]
    dim = getHeaderName(option,i)
    if dim == '--':
      continue
    else :
      fprint('\nChecking ' + dim)
      fprint( "_"*20 )
      header = list()
      file.seek(0)
      if ',' in file.readline():
        delim = ','
      elif ';' in file.readline():
        delim = ';'
      file.seek(0)
      for a in file.readline().split(delim):
        header.append(a.strip().strip('"').strip('"'))
      dimension = header.index(dim)
      file.seek(0)
      DataCaptured.next()
      for row in DataCaptured:
        distinctDim.add(row[dimension])
      distinctDim = list(distinctDim)
      if not list(set(distinctDim) - set(siaVals)):
        fprint( "\n\tSUCCESS" )
      else:
        fprint( '\n\t'+ dim + ' values are not okay')
        fprint( '\n\tExpected : ' + ', '.join(sorted(siaVals)))
        fprint( '\n\tGot      : ' + ', '.join(sorted(distinctDim)))
      if len(list(set(distinctDim) - set(siaVals))) > 0:
        fprint( '\n\tNew Values  : ' +', '.join(list(set(distinctDim) - set(siaVals))) )
      if len(list(set(siaVals) - set(distinctDim))) > 0:
        fprint( '\n\tDid not come: ' + ', '.join(list(set(siaVals) - set(distinctDim)) ))



def exit_program():
  exit()

def fprint(output):
  print output
  with open("MIPFileValidator.log", "a") as f:
    f.write("{}\n".format(output))
  return output
  
def open_file():
  fprint( "\n\nEnter complete file path below:\n" )
  path = fprint(raw_input().strip(' '))
  file = open(path, 'rU')
  file.seek(0)
  if ',' in file.readline():
    delim = ','
  elif ';' in file.readline():
    delim = ';'
  file.seek(0)
  DataCaptured = csv.reader(file, delimiter=delim, skipinitialspace=True)
  return file, DataCaptured

def close_file(file):
  file.close()

def checkDistinctValues():

  file, DataCaptured = open_file()
  headerString = next(DataCaptured)
  headerDict = {}
  key = 0
  fprint( "\nBelow are the columns present in the file :\n" )
  for header in headerString :
    key = key + 1
    headerDict [key] = header
  fprint( 'Index\t\tHeader' )
  fprint( '_'*8+'\t'+'_'*8 )
  for key in headerDict:
    fprint( str(key) +'\t:\t' + headerDict [key] ) 


  session = True
  while session :
    distinctDim = set()
    fprint( "\nEnter the index of the header whose distinct values you want to see, enter 0 to go to main menu\n" )
    dimension = int(raw_input())
    if dimension == 0:
      session = False
      main()
    else:
      file.seek(0)
      DataCaptured.next()
      for row in DataCaptured:
        distinctDim.add(row[dimension-1])
      fprint( '\n' )
      fprint( headerDict[dimension] )
      fprint( '_'*20 )
      for a in sorted(distinctDim):
        fprint( '\t' + a )

  close_file(file)


def variables():

  variables.files         =  [('idc_pc_chnl', 'IDC PC Channel File')
                             ,('idc_pc_seg' , 'IDC PC Segment File')
                             ,('idc_phone_chnl' , 'IDC Phone Channel File')
                             ,('idc_phone_seg' , 'IDC Phone Segment File')
                             ,('idc_tablet_chnl' , 'IDC Tablet Channel File')
                             ,('idc_tablet_seg' , 'IDC Tablet Segment File')
                             ,('idc_pc_chnl_forecast' , 'IDC PC Channel Forecast File')
                             ,('idc_pc_seg_forecast' , 'IDC PC Segment Forecast File')
                             ,('idc_phone_chnl_forecast' , 'IDC Phone Channel Forecast File')
                             ,('idc_phone_seg_forecast' , 'IDC Phone Segment Forecast File')
                             ,('idc_tablet_chnl_forecast' , 'IDC Tablet Channel Forecast File')
                             ,('idc_tablet_seg_forecast' , 'IDC Tablet Segment Forecast File')
                             ,('gfk_phone' , 'GFK Phone File')
                             ,('gfk_tablet' , 'GFK Tablet File')
                              ]

  variables.headername      =  {'idc_pc_chnl'               : [('Region','Region'),('Country','Country'),('Prod_lvl_2','Product Category'),('Prod_lvl_3','Product'),('Channel','Channel'),('Segment','--'),('Price_Band','Price Band')]
                               ,'idc_pc_seg'                : [('Region','Region'),('Country','Country'),('Prod_lvl_2','Product Category'),('Prod_lvl_3','Product'),('Channel','--'),('Segment','Segment'),('Price_Band','Price Band')]
                               ,'idc_phone_chnl'            : [('Region','Region'),('Country','Country'),('Prod_lvl_2','Form Factor'),('Prod_lvl_3','Product Category'),('Channel','Channel'),('Segment','--'),('Price_Band','Price Band')]
                               ,'idc_phone_seg'             : [('Region','Region'),('Country','Country'),('Prod_lvl_2','Form Factor'),('Prod_lvl_3','Product Category'),('Channel','--'),('Segment','Segment'),('Price_Band','Price Band')]
                               ,'idc_tablet_chnl'           : [('Region','Region'),('Country','Country'),('Prod_lvl_2','--'),('Prod_lvl_3','Form Factor'),('Channel','Channel'),('Segment','--'),('Price_Band','Price Band')]
                               ,'idc_tablet_seg'            : [('Region','Region'),('Country','Country'),('Prod_lvl_2','--'),('Prod_lvl_3','Form Factor'),('Channel','--'),('Segment','Segment'),('Price_Band','Price Band')]
                               ,'idc_pc_chnl_forecast'      : [('Region','Region'),('Country','Country'),('Prod_lvl_2','Product Category'),('Prod_lvl_3','Product'),('Channel','Channel'),('Segment','--'),('Price_Band','--')]  
                               ,'idc_pc_seg_forecast'       : [('Region','Region'),('Country','Country'),('Prod_lvl_2','Product Category'),('Prod_lvl_3','Product'),('Channel','--'),('Segment','Segment'),('Price_Band','--')]
                               ,'idc_phone_chnl_forecast'   : [('Region','Region'),('Country','Country'),('Prod_lvl_2','--'),('Prod_lvl_3','Product Category'),('Channel','Channel'),('Segment','--'),('Price_Band','Price Band')]
                               ,'idc_phone_seg_forecast'    : [('Region','Region'),('Country','Country'),('Prod_lvl_2','--'),('Prod_lvl_3','Product Category'),('Channel','--'),('Segment','--'),('Price_Band','--')]
                               ,'idc_tablet_chnl_forecast'  : [('Region','Region'),('Country','Country'),('Prod_lvl_2','--'),('Prod_lvl_3','--'),('Channel','Channel'),('Segment','--'),('Price_Band','--')]
                               ,'idc_tablet_seg_forecast'   : [('Region','Region'),('Country','Country'),('Prod_lvl_2','--'),('Prod_lvl_3','--'),('Channel','--'),('Segment','Segment'),('Price_Band','--')]
                               ,'gfk_phone'                 : [('Region','Region'),('Country','Country'),('Prod_lvl_2','--'),('Prod_lvl_3','--'),('Channel','--'),('Segment','Segment'),('Price_Band','NSP Pricebands USD')]
                               ,'gfk_tablet'                : [('Region','Region'),('Country','Country'),('Prod_lvl_2','--'),('Prod_lvl_3','--'),('Channel','--'),('Segment','Segment'),('Price_Band','NSP Pricebands USD')]
                              }


  variables.delimiter_map   =  {'idc_pc_chnl'               : ','
                               ,'idc_pc_seg'                : ','
                               ,'idc_phone_chnl'            : ','
                               ,'idc_phone_seg'             : ','
                               ,'idc_tablet_chnl'           : ','
                               ,'idc_tablet_seg'            : ','
                               ,'idc_pc_chnl_forecast'      : ','
                               ,'idc_pc_seg_forecast'       : ','
                               ,'idc_phone_chnl_forecast'   : ','
                               ,'idc_phone_seg_forecast'    : ','
                               ,'idc_tablet_chnl_forecast'  : ','
                               ,'idc_tablet_seg_forecast'   : ','
                               ,'gfk_phone'                 : ';'
                               ,'gfk_tablet'                : ';'
                                }

  variables.headerList      =  {'idc_pc_chnl'               : ['Quarter','Region','Country','Product Category','Product','Product Detail','Vendor','Vendor Group','OS','Product Brand','Price Band','Screen Size Band','Channel_Group','Channel','Units','Value (USD)']
                               ,'idc_pc_seg'                : ['Quarter','Region','Country','Product Category','Product','Product Detail','Vendor','Vendor Group','OS','Product Brand','Price Band','Screen Size Band','Segment Group','Segment','Units','Value (USD)']
                               ,'idc_phone_chnl'            : ['Region','Country','Country Code','Vendor','Product Category','Units','Value (US$M)','Price Band','Air Interface','Bluetooth','Dual SIM','Embedded Memory Band','Product Detail','Generation','Input Method','Megapixels Band','OS','OS Version','Quarter','Quarter 2','Year','Primary Memory Card','Processor Vendor','Processor Speed Band','Processor Cores','Screen Size','Screen Size Band','Channel Group','Smartphone Class','TV','WiFi','Form Factor','Bluetooth LE','RAM Band (GB)','Screen Resolution','Channel']
                               ,'idc_phone_seg'             : ['Region','Country','Country Code','Vendor','Product Category','Units','Value (US$M)','Price Band','Air Interface','Bluetooth','Dual SIM','Embedded Memory Band','Product Detail','Generation','Input Method','Megapixels Band','OS','OS Version','Quarter','Quarter 2','Year','Primary Memory Card','Processor Vendor','Processor Speed Band','Processor Cores','Screen Size','Screen Size Band','Segment Group','Smartphone Class','TV','WiFi','Form Factor','Bluetooth LE','RAM Band (GB)','Screen Resolution','Segment']
                               ,'idc_tablet_chnl'           : ['Region','Country','Quarter','Vendor','Form Factor','Connectivity','OS','CPU Type','Screen Size','Screen Size Band Historical','Screen Resolution','Storage (GB)','Channel','Units','Value (US$M)','Price Band','Year','RAM (GB)','Air Interface','Generation']
                               ,'idc_tablet_seg'            : ['Region','Country','Quarter','Vendor','Form Factor','Connectivity','OS','CPU Type','Screen Size','Screen Size Band Historical','Screen Resolution','Storage (GB)','Segment Group','Units','Value (US$M)','Price Band','Year','Product Category','RAM (GB)','Air Interface','Generation','Segment']
                               ,'idc_pc_chnl_forecast'      : []
                               ,'idc_pc_seg_forecast'       : ['Reporting Qtr','Year','Quarter','Region','Country','Product Category','Product','Operating System','Segment Group','Segment','Units','Value (USD M)','ASP (USD)']
                               ,'idc_phone_chnl_forecast'   : []
                               ,'idc_phone_seg_forecast'    : ['Reporting Qtr','Year','Quarter','Region','Country','Product Category','OS','Segment Group','Units','Value (USD M)','ASP (USD)']
                               ,'idc_tablet_chnl_forecast'  : ['Reporting Qtr','Region','Country','Year','Quarter','Product Category','OS','Channel Group','Channel','Units','Value (USD M)','ASP (USD)']
                               ,'idc_tablet_seg_forecast'   : ['Reporting Qtr','Region','Country','Year','Quarter','Product Category','OS','Segment Group','Segment','Units','Value (USD M)','ASP (USD)']
                               ,'gfk_phone'                 : ['FileType' ,'Period' ,'Quarter' ,'Year' ,'Country' ,'Region' ,'ReportingChannel' ,'DISTRIBUTIO_TYP' ,'BRAND' ,'Product' ,'PREPAID/POSTPAID*' ,'WAY OF BUYING' ,'OPERATOR' ,'OPERATING SYST.' ,'OS VERSION' ,'GENERATION TOTAL*' ,'NEAR FIELD COMM' ,'DISPLAY SIZE' ,'EDGE' ,'HSDPA' ,'HSPA+' ,'STORAGE IN GB' ,'NSP Pricebands EUR' ,'NSP Pricebands USD' ,'Retail Pricebands EUR' ,'Retail Pricebands USD' ,'SALES UNITS' ,'SALES USD' ,'SALES EUR' ,'SALES <LC>' ,'SV NONSUBS EST. EUR' ,'SV NONSUBS EST. USD' ,'SV NONSUBS EST. <LC>']
                               ,'gfk_tablet'                : ['FileType' ,'Period' ,'Quarter' ,'Year' ,'Country' ,'Region' ,'ReportingChannel' ,'Brand' ,'Item' ,'DISPLAY SIZE' ,'EMBEDDED 3G/4G' ,'OPERATING SYST.' ,'PROCESSOR' ,'PROCESSOR BRAND' ,'STORAGE IN GB' ,'NSP Pricebands EUR' ,'NSP Pricebands USD' ,'Retail Pricebands EUR' ,'Retail Pricebands USD' ,'SALES UNITS' ,'SALES USD' ,'SALES EUR' ,'SALES <LC>' ,'SV NONSUBS EST. USD' ,'SV NONSUBS EST. EUR' ,'SV NONSUBS EST. <LC>']
                                }

  variables.region_map      =  {'idc_pc_chnl'               : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                               ,'idc_pc_seg'                : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                               ,'idc_phone_chnl'            : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                               ,'idc_phone_seg'             : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                               ,'idc_tablet_chnl'           : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                               ,'idc_tablet_seg'            : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                               ,'idc_pc_chnl_forecast'      : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                               ,'idc_pc_seg_forecast'       : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                               ,'idc_phone_chnl_forecast'   : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                               ,'idc_phone_seg_forecast'    : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                               ,'idc_tablet_chnl_forecast'  : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                               ,'idc_tablet_seg_forecast'   : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                               ,'gfk_phone'                 : ['ASIA' ,'EUROPE' ,'LATAM' ,'MIDEAST/AFRICA']
                               ,'gfk_tablet'                : ['ASIA' ,'EUROPE' ,'LATAM' ,'MIDEAST/AFRICA']
                                }

#TODO Verify Countries for GFK
  variables.country_map     =  {'idc_pc_chnl'               : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'idc_pc_seg'                : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'idc_phone_chnl'            : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'idc_phone_seg'             : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'idc_tablet_chnl'           : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'idc_tablet_seg'            : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'idc_pc_chnl_forecast'      : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'idc_pc_seg_forecast'       : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'idc_phone_chnl_forecast'   : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'idc_phone_seg_forecast'    : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'idc_tablet_chnl_forecast'  : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'idc_tablet_seg_forecast'   : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'gfk_phone'                 : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'gfk_tablet'                : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                                }

  variables.prod_lvl_2_map =   {'idc_pc_chnl'               : ['Desktop PC' ,'Portable PC']
                               ,'idc_pc_seg'                : ['Desktop PC' ,'Portable PC']
                               ,'idc_phone_chnl'            : ['Mobile Phones']
                               ,'idc_phone_seg'             : ['Mobile Phones']
                               ,'idc_tablet_chnl'           : ['7"<9"' ,'9"+' ,'<7"']
                               ,'idc_tablet_seg'            : ['7"<9"' ,'9"+' ,'<7"']
                               ,'idc_pc_chnl_forecast'      : ['Desktop PC' ,'Portable PC']
                               ,'idc_pc_seg_forecast'       : ['Desktop PC' ,'Portable PC']
                               ,'idc_phone_chnl_forecast'   : ['Mobile Phones']
                               ,'idc_phone_seg_forecast'    : ['Mobile Phones']
                               ,'idc_tablet_chnl_forecast'  : ['7"<9"' ,'9"+' ,'<7"']
                               ,'idc_tablet_seg_forecast'   : ['7"<9"' ,'9"+' ,'<7"']
                               ,'gfk_phone'                 : []
                               ,'gfk_tablet'                : []
                                    }

  variables.prod_lvl_3_map=    {'idc_pc_chnl'               : ['All in One PC' ,'Convertible Notebook PC' ,'Mini Notebook PC' ,'Traditional Desktop PC' ,'Traditional Notebook PC' ,'Ultraslim Notebook PC']
                               ,'idc_pc_seg'                : ['All in One PC' ,'Convertible Notebook PC' ,'Mini Notebook PC' ,'Traditional Desktop PC' ,'Traditional Notebook PC' ,'Ultraslim Notebook PC']
                               ,'idc_phone_chnl'            : ['Smartphone' ,'Feature Phone']
                               ,'idc_phone_seg'             : ['Smartphone' ,'Feature Phone']
                               ,'idc_tablet_chnl'           : ['2-in-1' ,'Tablet','eReader']
                               ,'idc_tablet_seg'            : ['2-in-1' ,'Tablet','eReader']
                               ,'idc_pc_chnl_forecast'      : ['All in One PC' ,'Convertible Notebook PC' ,'Mini Notebook PC' ,'Traditional Desktop PC' ,'Traditional Notebook PC' ,'Ultraslim Notebook PC']
                               ,'idc_pc_seg_forecast'       : ['All in One PC' ,'Convertible Notebook PC' ,'Mini Notebook PC' ,'Traditional Desktop PC' ,'Traditional Notebook PC' ,'Ultraslim Notebook PC']
                               ,'idc_phone_chnl_forecast'   : ['Smartphone' ,'Feature Phone']
                               ,'idc_phone_seg_forecast'    : ['Smartphone' ,'Feature Phone']
                               ,'idc_tablet_chnl_forecast'  : ['2-in-1' ,'Tablet','eReader']
                               ,'idc_tablet_seg_forecast'   : ['2-in-1' ,'Tablet','eReader']
                               ,'gfk_phone'                 : []
                               ,'gfk_tablet'                : []
                                    }

  variables.channel_map     =  {'idc_pc_chnl'               : ['Dealer/VAR/SI' ,'Retail' ,'Telco' ,'Vendor Direct - Internet' ,'Vendor Direct - Relationship' ,'Vendor Direct - Store' ,'Vendor Direct - Transactional' ,'eTailer']
                               ,'idc_pc_seg'                : []
                               ,'idc_phone_chnl'            : ['Direct' ,'Others' ,'Retail' ,'Telco' ,'eTailer']
                               ,'idc_phone_seg'             : []
                               ,'idc_tablet_chnl'           : ['eTailer' ,'Others' ,'Retail' ,'Telco' ,'Vendor Direct - Others' ,'Vendor Direct - Store']
                               ,'idc_tablet_seg'            : []
                               ,'idc_pc_chnl_forecast'      : ['Dealer/VAR/SI' ,'Retail' ,'Telco' ,'Vendor Direct - Internet' ,'Vendor Direct - Relationship' ,'Vendor Direct - Store' ,'Vendor Direct - Transactional' ,'eTailer']
                               ,'idc_pc_seg_forecast'       : []
                               ,'idc_phone_chnl_forecast'   : ['Direct' ,'Others' ,'Retail' ,'Telco' ,'eTailer']
                               ,'idc_phone_seg_forecast'    : []
                               ,'idc_tablet_chnl_forecast'  : ['eTailer' ,'Others' ,'Retail' ,'Telco' ,'Vendor Direct - Others' ,'Vendor Direct - Store']
                               ,'idc_tablet_seg_forecast'   : []
                               ,'gfk_phone'                 : ['INTERNET SALES' ,'TOTAL' ,'TRADITIONAL (NON-INTERNET)']
                               ,'gfk_tablet'                : ['CES' ,'CS' ,'MASSMERCH/DIYSS' ,'OER/TCR' ,'PANELMARKET' ,'RESELL' ,'RETAIL' ,'SH']
                                    }

  variables.segment_map     =  {'idc_pc_chnl'               : []
                               ,'idc_pc_seg'                : ['Consumer' ,'Education' ,'Government' ,'Large Business (500-999)' ,'Medium Business (100-499)' ,'Small Business (10-99)' ,'Small Office (1-9)' ,'Very Large Business (1000+)']
                               ,'idc_phone_chnl'            : []
                               ,'idc_phone_seg'             : ['Commercial' ,'Consumer' ,'Education' ,'Government' ,'Large Business (500-999)' ,'Medium Business (100-499)' ,'Small Business (10-99)' ,'Small Office (1-9)' ,'Very Large Business (1000+)'] #TODO Confirmation Required of Values.
                               ,'idc_tablet_chnl'           : []
                               ,'idc_tablet_seg'            : ['Commercial' ,'Consumer' ,'Education' ,'Government' ,'Large Business (500-999)' ,'Medium Business (100-499)' ,'Small Business (10-99)' ,'Small Office (1-9)' ,'Very Large Business (1000+)']
                               ,'idc_pc_chnl_forecast'      : []
                               ,'idc_pc_seg_forecast'       : ['Consumer' ,'Education' ,'Government' ,'Large Business (500-999)' ,'Medium Business (100-499)' ,'Small Business (10-99)' ,'Small Office (1-9)' ,'Very Large Business (1000+)']
                               ,'idc_phone_chnl_forecast'   : []
                               ,'idc_phone_seg_forecast'    : ['Consumer' ,'Education' ,'Government' ,'Large Business (500-999)' ,'Medium Business (100-499)' ,'Small Business (10-99)' ,'Small Office (1-9)' ,'Very Large Business (1000+)']
                               ,'idc_tablet_chnl_forecast'  : []
                               ,'idc_tablet_seg_forecast'   : ['Consumer' ,'Education' ,'Government' ,'Large Business (500-999)' ,'Medium Business (100-499)' ,'Small Business (10-99)' ,'Small Office (1-9)' ,'Very Large Business (1000+)']
                               ,'gfk_phone'                 : []
                               ,'gfk_tablet'                : []
                                    }


  variables.price_band_map  =  {'idc_pc_chnl'               : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                               ,'idc_pc_seg'                : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                               ,'idc_phone_chnl'            : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                               ,'idc_phone_seg'             : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                               ,'idc_tablet_chnl'           : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                               ,'idc_tablet_seg'            : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                               ,'idc_pc_chnl_forecast'      : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                               ,'idc_pc_seg_forecast'       : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                               ,'idc_phone_chnl_forecast'   : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                               ,'idc_phone_seg_forecast'    : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                               ,'idc_tablet_chnl_forecast'  : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                               ,'idc_tablet_seg_forecast'   : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                               ,'gfk_phone'                 : ['0 < 100 USD' ,'100 < 200 USD' ,'200 < 300 USD' ,'300 < 400 USD' ,'400 < 500 USD' ,'500 < 600 USD' ,'600 < 700 USD' ,'>= 700 USD','TOTAL']
                               ,'gfk_tablet'                : ['0 < 100 USD' ,'100 < 200 USD' ,'200 < 300 USD' ,'300 < 400 USD' ,'400 < 500 USD' ,'500 < 600 USD' ,'600 < 700 USD' ,'>= 700 USD','TOTAL']
                                    }


if __name__ == '__main__':
  main()


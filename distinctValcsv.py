import csv
import sys
import os

def main():

  fprint( "\n\nEnter number corresponding to the operation you want to perform")
  fprint( "_"*70)
  fprint( "\n\t1 - Check distinct Values" )
  fprint( "\t2 - Validate File" ) 
  fprint( "\t3 - Exit" )
  try:
    option = int(raw_input())
    if option == 1 :
      checkDistinctValues()
    elif option == 2 :
      validateFile()
    elif option == 3 :
      exit_program()
  except  :
    e = sys.exc_info()
    fprint( e )

def fprint(output):
  print output
  with open("MIPFileValidator.log", "a") as f:
    f.write("{}\n".format(output))
  
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

def file_type():

  fprint( "\nWhich file you want to validate . Enter corresponding number .\n ")
  fprint( "\t1. IDC PC Channel")
  fprint( "\t2. IDC PC Segment")
  fprint( "\t3. IDC Phone Channel")
  fprint( "\t4. IDC Phone Segment")
  fprint( "\t5. IDC Tablet Channel")
  fprint( "\t6. IDC Tablet Segment")
  fprint( "\t7. GFK Phone")
  fprint( "\t8. GFK Tablet")

  option = int(raw_input())
  return option


def validateFile():
  option = file_type()
  file, DataCaptured = open_file()
  validateDelimiter(option,file, DataCaptured)
  validateHeader(option,file, DataCaptured)
  validateRegion(option,file, DataCaptured)
  validateCountry(option,file, DataCaptured)
  validateProd_lvl_2(option,file, DataCaptured)
  validateProd_lvl_3(option,file, DataCaptured)  
  validateChannel(option,file, DataCaptured)
  validateSegment(option,file, DataCaptured)
  validatePriceBand(option,file, DataCaptured)

  close_file(file)
  main()

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
    fprint( "\n\tFAILURE : See Logs" )
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
#   if list(set(header) - set(siaHeader)) is not []:
#     fprint( "\n\tNew Columns are there : " ,list(set(header) - set(siaHeader))

def validateRegion(option,file, DataCaptured):
  fprint( "\nChecking Region.." )
  fprint( "_"*20 )
  variables()
  siaVals = variables.region_map[variables.files[option - 1][0]]
  distinctDim = set()
  file.seek(0)
  dictKey = variables.files[option - 1][0]
  dim = 'Region'
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
    fprint( "\n\tRegion values are not okay" )
    fprint( '\n\tExpected : ' + ', '.join(sorted(siaVals)))
    fprint( '\n\tGot      : ' + ', '.join(sorted(distinctDim)))
  if len(list(set(distinctDim) - set(siaVals))) > 0:
    fprint( '\n\tNew Values  : ' +', '.join(list(set(distinctDim) - set(siaVals))) )
  if len(list(set(siaVals) - set(distinctDim))) > 0:
    fprint( '\n\tDid not come: ' + ', '.join(list(set(siaVals) - set(distinctDim)) ))


def validateCountry(option,file, DataCaptured):
  fprint( "\nChecking Country.." )
  fprint( "_"*20 )
  variables()
  siaVals = variables.country_map[variables.files[option - 1][0]]
  distinctDim = set()
  file.seek(0)
  dictKey = variables.files[option - 1][0]
  dim = 'Country'
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
    fprint( "\n\tCountry values are not okay" )
    fprint( '\n\tExpected : ' + ', '.join(sorted(siaVals)))
    fprint( '\n\tGot      : ' + ', '.join(sorted(distinctDim)))
  if len(list(set(distinctDim) - set(siaVals))) > 0:
    fprint( '\n\tNew Values  : ' +', '.join(list(set(distinctDim) - set(siaVals))) )
  if len(list(set(siaVals) - set(distinctDim))) > 0:
    fprint( '\n\tDid not come: ' + ', '.join(list(set(siaVals) - set(distinctDim)) ))

def validateProd_lvl_2(option,file, DataCaptured):
  fprint( "\nChecking Prod_lvl_2.." )
  fprint( "_"*20 )
  variables()
  siaVals = variables.prod_lvl_2_map[variables.files[option - 1][0]]
  distinctDim = set()
  file.seek(0)
  dictKey = variables.files[option - 1][0]
  if option in [1,2]:
    dim = 'Product Category'
  elif option in [3,4]:
    dim = 'Form Factor'
  else :
    dim = '--'
  if dim == '--':
    fprint('\n\tProd_lvl_2 not applicable')
  else :
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
      fprint( "\n\tProd_lvl_2 values are not okay" )
      fprint( '\n\tExpected : ' + ', '.join(sorted(siaVals)))
      fprint( '\n\tGot      : ' + ', '.join(sorted(distinctDim)))
    if len(list(set(distinctDim) - set(siaVals))) > 0:
      fprint( '\n\tNew Values  : ' +', '.join(list(set(distinctDim) - set(siaVals))) )
    if len(list(set(siaVals) - set(distinctDim))) > 0:
      fprint( '\n\tDid not come: ' + ', '.join(list(set(siaVals) - set(distinctDim)) ))


def validateProd_lvl_3(option,file, DataCaptured):
  fprint( "\nChecking Prod_lvl_3.." )
  fprint( "_"*20 )
  variables()
  siaVals = variables.prod_lvl_3_map[variables.files[option - 1][0]]
  distinctDim = set()
  file.seek(0)
  dictKey = variables.files[option - 1][0]
  if option in [1,2]:
    dim = 'Product'
  elif option in [3,4] :
    dim = 'Product Category'
  elif option in [5,6] :
    dim = 'Form Factor'
  else :
    dim = '--'
  if dim == '--':
    fprint('\n\tProd_lvl_3 not applicable')
  else :
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
      fprint( "\n\tProd_lvl_3 values are not okay" )
      fprint( '\n\tExpected : ' + ', '.join(sorted(siaVals)))
      fprint( '\n\tGot      : ' + ', '.join(sorted(distinctDim)))
    if len(list(set(distinctDim) - set(siaVals))) > 0:
      fprint( '\n\tNew Values  : ' +', '.join(list(set(distinctDim) - set(siaVals))) )
    if len(list(set(siaVals) - set(distinctDim))) > 0:
      fprint( '\n\tDid not come: ' + ', '.join(list(set(siaVals) - set(distinctDim)) ))



def validateChannel(option,file, DataCaptured):
  fprint( "\nChecking Channel.." )
  fprint( "_"*20 )
  variables()
  siaVals = variables.channel_map[variables.files[option - 1][0]]
  distinctDim = set()
  file.seek(0)
  dictKey = variables.files[option - 1][0]
  if option in [1,3,5]:
    dim = 'Channel'
  elif option == 7 :
    dim = 'DISTRIBUTIO_TYP'
  elif option == 8 :
    dim = 'ReportingChannel'
  else :
    dim = '--'
  if dim == '--':
    fprint('\n\tChannel not applicable')
  else :
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
      fprint( "\n\tChannel values are not okay" )
      fprint( '\n\tExpected : ' + ', '.join(sorted(siaVals)))
      fprint( '\n\tGot      : ' + ', '.join(sorted(distinctDim)))
    if len(list(set(distinctDim) - set(siaVals))) > 0:
      fprint( '\n\tNew Values  : ' +', '.join(list(set(distinctDim) - set(siaVals))) )
    if len(list(set(siaVals) - set(distinctDim))) > 0:
      fprint( '\n\tDid not come: ' + ', '.join(list(set(siaVals) - set(distinctDim)) ))


def validateSegment(option,file, DataCaptured):
  fprint( "\nChecking Segment.." )
  fprint( "_"*20 )
  variables()
  siaVals = variables.segment_map[variables.files[option - 1][0]]
  distinctDim = set()
  file.seek(0)
  dictKey = variables.files[option - 1][0]
  if option in [2,4,6]:
    dim = 'Segment'
#   elif option == 4 :         TODO : Confirmation Required for IDC Phone Segment File, name of header .
#     dim = 'Segment Group'
  else :
    dim = '--'
  if dim == '--':
    fprint('\n\tSegment not applicable')
  else :
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
      fprint( "\nSegment values are not okay" )
      fprint( '\n\tExpected : ' + ', '.join(sorted(siaVals)))
      fprint( '\n\tGot      : ' + ', '.join(sorted(distinctDim)))
    if len(list(set(distinctDim) - set(siaVals))) > 0:
      fprint( '\n\tNew Values  : ' +', '.join(list(set(distinctDim) - set(siaVals))) )
    if len(list(set(siaVals) - set(distinctDim))) > 0:
      fprint( '\n\tDid not come: ' + ', '.join(list(set(siaVals) - set(distinctDim)) ))

def validatePriceBand(option,file, DataCaptured):
  fprint( "\nChecking Price Band.." )
  fprint( "_"*20 )
  variables()
  siaVals = variables.price_band_map[variables.files[option - 1][0]]
  distinctDim = set()
  file.seek(0)
  dictKey = variables.files[option - 1][0]
  if option in [1,2,3,4,5,6]:
    dim = 'Price Band'
  elif option in [7,8]:
    dim = 'NSP Pricebands USD'
  else :
    dim = '--'
  if dim == '--':
    fprint('\n\tPrice Band not applicable')
  else :
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
      fprint( "\nPrice Band values are not okay" )
      fprint( '\n\tExpected : ' + ', '.join(sorted(siaVals)))
      fprint( '\n\tGot      : ' + ', '.join(sorted(distinctDim)))
    if len(list(set(distinctDim) - set(siaVals))) > 0:
      fprint( '\n\tNew Values  : ' +', '.join(list(set(distinctDim) - set(siaVals))) )
    if len(list(set(siaVals) - set(distinctDim))) > 0:
      fprint( '\n\tDid not come: ' + ', '.join(list(set(siaVals) - set(distinctDim)) ))

def exit_program():
  exit()

def variables():

  variables.files         =  [('idc_pc_chnl', 'IDC PC Channel File')
                             ,('idc_pc_seg' , 'IDC PC Segment File')
                             ,('idc_phone_chnl' , 'IDC Phone Channel File')
                             ,('idc_phone_seg' , 'IDC Phone Segment File')
                             ,('idc_tablet_chnl' , 'IDC Tablet Channel File')
                             ,('idc_tablet_seg' , 'IDC Tablet Segment File')
                             ,('gfk_phone' , 'GFK Phone File')
                             ,('gfk_tablet' , 'GFK Tablet File')
                              ]


  variables.delimiter_map     =  {'idc_pc_chnl'     : ','
                                 ,'idc_pc_seg'      : ','
                                 ,'idc_phone_chnl'  : ','
                                 ,'idc_phone_seg'   : ','
                                 ,'idc_tablet_chnl' : ','
                                 ,'idc_tablet_seg'  : ','
                                 ,'gfk_phone'       : ';'
                                 ,'gfk_tablet'      : ';'
                                  }

  variables.headerList      =  {'idc_pc_chnl'     : ['Region','Country','Form Factor','Product Category','Vendor','Brand','Segment','Period','Units','Value (USD)','Price Band']
                               ,'idc_pc_seg'      : ['Region','Country','Form Factor','Product Category','Vendor','Brand','Segment','Period','Units','Value (USD)','Price Band']
                               ,'idc_phone_chnl'  : ['Region','Country Code','Country','Vendor','Product Category','Units','Value (M)','Priceband','Air Interface','Bluetooth','Brew','Display Type','Dual SIM','Embedded Memory Band','Device Stye','Generation','GPS','Input Method','Java','Megapixels Band','MMS','Music Player','NFC','Operating System','Platform','OS Version','Period','Period 2','Primary Memory Card','Processor Vendor','Processor Speed Band','Processor Cores','Push2Talk','Radio','Screen Size','Screen Size Bands','Smartphone Tier','TV','Video Player','Voip','WiFi','Annual','Form Factor']
                               ,'idc_phone_seg'   : ['Region','Country Code','Country','Vendor','Product Category','Units','Value (M)','Priceband','Air Interface','Bluetooth','Brew','Display Type','Dual SIM','Embedded Memory Band','Device Stye','Generation','GPS','Input Method','Java','Megapixels Band','MMS','Music Player','NFC','Operating System','Platform','OS Version','Period','Period 2','Primary Memory Card','Processor Vendor','Processor Speed Band','Processor Cores','Push2Talk','Radio','Screen Size','Screen Size Bands','Smartphone Tier','TV','Video Player','Voip','WiFi','Annual','Form Factor']
                               ,'idc_tablet_chnl' : ['Region','Country','Period','Vendor','Form Factor','Connectivity','OS','CPU Type','Screen Size (in.)','Screen Size Band','Screen Resolution','Storage (GB)','Channel','Units','Value (US$M) (USD)','Priceband','Annual','Product Category']
                               ,'idc_tablet_seg'  : ['Region','Country','Period','Vendor','Form Factor','Connectivity','OS','CPU Type','Screen Size (in.)','Screen Size Band','Screen Resolution','Storage (GB)','segment','Units','Value (US$M) (USD)','Priceband','Annual','Product Category']
                               ,'gfk_phone'       : ['FileType' ,'Period' ,'Quarter' ,'Year' ,'Country' ,'Region' ,'ReportingChannel' ,'DISTRIBUTIO_TYP' ,'BRAND' ,'Product' ,'PREPAID/POSTPAID*' ,'WAY OF BUYING' ,'OPERATOR' ,'OPERATING SYST.' ,'OS VERSION' ,'GENERATION TOTAL*' ,'NEAR FIELD COMM' ,'DISPLAY SIZE' ,'EDGE' ,'HSDPA' ,'HSPA+' ,'STORAGE IN GB' ,'NSP Pricebands EUR' ,'NSP Pricebands USD' ,'Retail Pricebands EUR' ,'Retail Pricebands USD' ,'SALES UNITS' ,'SALES USD' ,'SALES EUR' ,'SALES <LC>' ,'SV NONSUBS EST. EUR' ,'SV NONSUBS EST. USD' ,'SV NONSUBS EST. <LC>']
                               ,'gfk_tablet'      : ['FileType' ,'Period' ,'Quarter' ,'Year' ,'Country' ,'Region' ,'ReportingChannel' ,'Brand' ,'Item' ,'DISPLAY SIZE' ,'EMBEDDED 3G/4G' ,'OPERATING SYST.' ,'PROCESSOR' ,'PROCESSOR BRAND' ,'STORAGE IN GB' ,'NSP Pricebands EUR' ,'NSP Pricebands USD' ,'Retail Pricebands EUR' ,'Retail Pricebands USD' ,'SALES UNITS' ,'SALES USD' ,'SALES EUR' ,'SALES <LC>' ,'SV NONSUBS EST. USD' ,'SV NONSUBS EST. EUR' ,'SV NONSUBS EST. <LC>']
                                }

  variables.region_map      =  {'idc_pc_chnl'     : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                               ,'idc_pc_seg'      : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                               ,'idc_phone_chnl'  : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                               ,'idc_phone_seg'   : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                               ,'idc_tablet_chnl' : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                               ,'idc_tablet_seg'  : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                               ,'gfk_phone'       : ['ASIA' ,'EUROPE' ,'LATAM' ,'MIDEAST/AFRICA']
                               ,'gfk_tablet'      : ['ASIA' ,'EUROPE' ,'LATAM' ,'MIDEAST/AFRICA']
                                }

  variables.country_map     =  {'idc_pc_chnl'     : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'idc_pc_seg'      : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'idc_phone_chnl'  : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'idc_phone_seg'   : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'idc_tablet_chnl' : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'idc_tablet_seg'  : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'gfk_phone'       : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                               ,'gfk_tablet'      : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                                }

  variables.prod_lvl_2_map =   {'idc_pc_chnl'     : ['Desktop PC' ,'Portable PC']
                               ,'idc_pc_seg'      : ['Desktop PC' ,'Portable PC']
                               ,'idc_phone_chnl'  : ['Mobile Phones']
                               ,'idc_phone_seg'   : ['Mobile Phones']
                               ,'idc_tablet_chnl' : ['7"<9"' ,'9"+' ,'<7"']
                               ,'idc_tablet_seg'  : ['7"<9"' ,'9"+' ,'<7"']
                               ,'gfk_phone'       : []
                               ,'gfk_tablet'      : []
                                    }

  variables.prod_lvl_3_map=    {'idc_pc_chnl'     : ['All in One PC' ,'Convertible Notebook PC' ,'Mini Notebook PC' ,'Traditional Desktop PC' ,'Traditional Notebook PC' ,'Ultraslim Notebook PC']
                               ,'idc_pc_seg'      : ['All in One PC' ,'Convertible Notebook PC' ,'Mini Notebook PC' ,'Traditional Desktop PC' ,'Traditional Notebook PC' ,'Ultraslim Notebook PC']
                               ,'idc_phone_chnl'  : ['Smartphone' ,'Feature phone']
                               ,'idc_phone_seg'   : ['Smartphone' ,'Feature phone']
                               ,'idc_tablet_chnl' : ['2-in-1' ,'Tablet','eReader']
                               ,'idc_tablet_seg'  : ['2-in-1' ,'Tablet','eReader']
                               ,'gfk_phone'       : []
                               ,'gfk_tablet'      : []
                                    }

  variables.channel_map     =  {'idc_pc_chnl'     : ['Dealer/VAR/SI' ,'Retail' ,'Telco' ,'Vendor Direct - Internet' ,'Vendor Direct - Relationship' ,'Vendor Direct - Store' ,'Vendor Direct - Transactional' ,'eTailer']
                               ,'idc_pc_seg'      : []
                               ,'idc_phone_chnl'  : ['Direct' ,'Others' ,'Retail' ,'Telco' ,'eTailer']
                               ,'idc_phone_seg'   : []
                               ,'idc_tablet_chnl' : ['eTailer' ,'Others' ,'Retail' ,'Telco' ,'Vendor Direct - Others' ,'Vendor Direct - Store']
                               ,'idc_tablet_seg'  : []
                               ,'gfk_phone'       : ['INTERNET SALES' ,'TOTAL' ,'TRADITIONAL (NON-INTERNET)']
                               ,'gfk_tablet'      : ['CES' ,'CS' ,'MASSMERCH/DIYSS' ,'OER/TCR' ,'PANELMARKET' ,'RESELL' ,'RETAIL' ,'SH']
                                    }

  variables.segment_map     =  {'idc_pc_chnl'     : []
                               ,'idc_pc_seg'      : ['Consumer' ,'Education' ,'Government' ,'Large Business (500-999)' ,'Medium Business (100-499)' ,'Small Business (10-99)' ,'Small Office (1-9)' ,'Very Large Business (1000+)']
                               ,'idc_phone_chnl'  : []
                               ,'idc_phone_seg'   : ['Commercial' ,'Consumer' ,'Education' ,'Government' ,'Large Business (500-999)' ,'Medium Business (100-499)' ,'Small Business (10-99)' ,'Small Office (1-9)' ,'Very Large Business (1000+)'] #TODO Confirmation Required of Values.
                               ,'idc_tablet_chnl' : []
                               ,'idc_tablet_seg'  : ['Commercial' ,'Consumer' ,'Education' ,'Government' ,'Large Business (500-999)' ,'Medium Business (100-499)' ,'Small Business (10-99)' ,'Small Office (1-9)' ,'Very Large Business (1000+)']
                               ,'gfk_phone'       : []
                               ,'gfk_tablet'      : []
                                    }


  variables.price_band_map  =  {'idc_pc_chnl'     : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                               ,'idc_pc_seg'      : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                               ,'idc_phone_chnl'  : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                               ,'idc_phone_seg'   : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                               ,'idc_tablet_chnl' : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                               ,'idc_tablet_seg'  : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                               ,'gfk_phone'       : ['0 < 100 USD' ,'100 < 200 USD' ,'200 < 300 USD' ,'300 < 400 USD' ,'400 < 500 USD' ,'500 < 600 USD' ,'600 < 700 USD' ,'>= 700 USD','TOTAL']
                               ,'gfk_tablet'      : ['0 < 100 USD' ,'100 < 200 USD' ,'200 < 300 USD' ,'300 < 400 USD' ,'400 < 500 USD' ,'500 < 600 USD' ,'600 < 700 USD' ,'>= 700 USD','TOTAL']
                                    }


if __name__ == '__main__':
  main()



import csv
import sys
import os

def main():

    print "\n\nEnter number corresponding to the operation you want to perform"
    print "_"*70
    print "\n\t1. Check distict Values"
    print "\t2. Validate File"
    print "\t3. Exit"
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

def open_file():

    print "\n\nEnter complete file path below:\n"
    path = raw_input().strip(' ')

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
    print "\nBelow are the columns present in the file :\n"
    for header in headerString :
        key = key + 1
        headerDict [key] = header
    print 'Index\t\tHeader'
    print '_'*8+'\t'+'_'*8
    for key in headerDict:
        print key ,'\t:\t',  headerDict [key]


    session = True
    while session :
        distinctDim = set()
        print "\nEnter the index of the header whose distinct values you want to see, enter 0 to go to main menu\n"
        dimension = int(raw_input())
        if dimension == 0:
            session = False
            main()
        else:
            file.seek(0)
            DataCaptured.next()
            for row in DataCaptured:
                distinctDim.add(row[dimension-1])
            print '\n'
            print headerDict[dimension]
            print '_'*20
            for a in sorted(distinctDim):
                print '\t',a

    close_file(file)

def file_type():

    print "\nWhich file you want to validate . Enter corresponding number .\n "
    print "\t1. IDC PC"
    print "\t2. IDC Phone"
    print "\t3. IDC Tablet Channel"
    print "\t4. IDC Tablet Segment"
    print "\t5. GFK Phone"
    print "\t6. GFK Tablet"
    
    option = int(raw_input())
    return option
    
    
def validateFile():
    option = file_type()
    file, DataCaptured = open_file()
    validateDelimiter(option,file, DataCaptured)
    validateHeader(option,file, DataCaptured)
    validateRegion(option,file, DataCaptured)
    validatePriceBand(option,file, DataCaptured)
    
    close_file(file)
    main()

def validateDelimiter(option,file, DataCaptured):
    variables()
    siaDelimiter = variables.delimiter_map[variables.files[option - 1]]
    print "\nChecking Delimiter.."
    print "_"*20
    file.seek(0)
    if ',' in file.readline():
        delim = ','
    elif ';' in file.readline():
        delim = ';'
    if siaDelimiter == delim :
        print "\n\tSUCCESS"
    else:
        print "Delimiter of files are not proper"
        print "\n\tExpected = " + siaDelimiter
        print "\tGot  = " + delim     

def validateHeader(option,file, DataCaptured):
    variables()
    siaHeader = variables.headerList[variables.files[option - 1]]
    file.seek(0)
    if ',' in file.readline():
        delim = ','
    elif ';' in file.readline():
        delim = ';'
    file.seek(0)
    header = list()
    for a in file.readline().split(delim):
        header.append(a.strip())
    print "\nChecking Header.."
    print "_"*20
    if siaHeader == header:
        print "\n\tSUCCESS"
    if len(list(set(header) - set(siaHeader))) > 0:
        print "\n\tHeaders are not proper"
        print '\nExpected : ' ,siaHeader
        print '\nGot      : ' ,header
#   if list(set(header) - set(siaHeader)) is not []:
#       print "\n\tNew Columns are there : " ,list(set(header) - set(siaHeader))
        
def validateRegion(option,file, DataCaptured):
    print "\nChecking Region.."
    print "_"*20
    variables()
    siaVals = variables.region_map[variables.files[option - 1]]
    distinctDim = set()
    file.seek(0)
    dictKey = variables.files[option - 1]
    if option in [1,2,3,4]:
        dim = 'Region'
    else:
        dim = '"Region"'
    dimension = variables.headerList.get(dictKey).index(dim)
    DataCaptured.next()
    for row in DataCaptured:
        distinctDim.add(row[dimension])
    distinctDim = list(distinctDim)
    if not list(set(distinctDim) - set(siaVals)):
        print "\n\tSUCCESS"
    else: 
        print "\nRegion values are not okay"
        print '\nExpected : ',siaVals
        print '\nGot      : ' ,distinctDim
    if len(list(set(distinctDim) - set(siaVals))) > 0:
        print '\n\tNew Values : ', list(set(distinctDim) - set(siaVals))
    if len(list(set(siaVals) - set(distinctDim))) > 0:
        print '\n\tDid not come: ', list(set(siaVals) - set(distinctDim))

def validatePriceBand(option,file, DataCaptured):
    print "\nChecking Price Band.."
    print "_"*20
    variables()
    siaVals = variables.price_band_map[variables.files[option - 1]]
    distinctDim = set()
    file.seek(0)
    dictKey = variables.files[option - 1]
    if option in [1]:
        dim = 'Price Band'
    elif option in [2,3,4] :
        dim = 'Priceband'
    else:
        dim = '"Retail Pricebands USD"'
    dimension = variables.headerList.get(dictKey).index(dim)
    DataCaptured.next()
    for row in DataCaptured:
        distinctDim.add(row[dimension])
    distinctDim = list(distinctDim)
    if not list(set(distinctDim) - set(siaVals)):
        print "\n\tSUCCESS"
    else: 
        print "\nRegion values are not okay"
        print '\nExpected : ',siaVals
        print '\nGot      : ' ,distinctDim
    if len(list(set(distinctDim) - set(siaVals))) > 0:
        print '\n\tNew Values : ', list(set(distinctDim) - set(siaVals))
    if len(list(set(siaVals) - set(distinctDim))) > 0:
        print '\n\tDid not come: ', list(set(siaVals) - set(distinctDim))


def exit_program():
    sys.exit(0)

def variables():
    
    variables.files               =  ['idc_pc','idc_phone','idc_tablet_chnl','idc_tablet_seg','gfk_phone','gfk_tablet']
    variables.delimiter_map       =  {'idc_pc' : ',' 
                                     ,'idc_phone' : ',' 
                                     ,'idc_tablet_chnl' : ',' 
                                     ,'idc_tablet_seg' : ',' 
                                     ,'gfk_phone' : ';' 
                                     ,'gfk_tablet' : ';'}

    variables.headerList          =  {'idc_pc'          : ['Region','Country','Form Factor','Product Category','Vendor','Brand','Segment','Period','Units','Value (USD)','Price Band']
                                     ,'idc_phone'       : ['Region','Country Code','Country','Vendor','Product Category','Units','Value (M)','Priceband','Air Interface','Bluetooth','Brew','Display Type','Dual SIM','Embedded Memory Band','Device Stye','Generation','GPS','Input Method','Java','Megapixels Band','MMS','Music Player','NFC','Operating System','Platform','OS Version','Period','Period 2','Primary Memory Card','Processor Vendor','Processor Speed Band','Processor Cores','Push2Talk','Radio','Screen Size','Screen Size Bands','Smartphone Tier','TV','Video Player','Voip','WiFi','Annual','Form Factor']
                                     ,'idc_tablet_chnl' : ['Region','Country','Period','Vendor','Form Factor','Connectivity','OS','CPU Type','Screen Size (in.)','Screen Size Band','Screen Resolution','Storage (GB)','Channel','Units','Value (US$M) (USD)','Priceband','Annual','Product Category']
                                     ,'idc_tablet_seg'  : ['Region','Country','Period','Vendor','Form Factor','Connectivity','OS','CPU Type','Screen Size (in.)','Screen Size Band','Screen Resolution','Storage (GB)','segment','Units','Value (US$M) (USD)','Priceband','Annual','Product Category']
                                     ,'gfk_phone'       : ['"FileType"' ,'"Period"' ,'"Quarter"' ,'"Year"' ,'"Country"' ,'"Region"' ,'"ReportingChannel"' ,'"DISTRIBUTIO_TYP"' ,'"BRAND"' ,'"Product"' ,'"PREPAID/POSTPAID*"' ,'"WAY OF BUYING"' ,'"OPERATOR"' ,'"OPERATING SYST."' ,'"OS VERSION"' ,'"GENERATION TOTAL*"' ,'"NEAR FIELD COMM"' ,'"DISPLAY SIZE"' ,'"EDGE"' ,'"HSDPA"' ,'"HSPA+"' ,'"STORAGE IN GB"' ,'"NSP Pricebands EUR"' ,'"NSP Pricebands USD"' ,'"Retail Pricebands EUR"' ,'"Retail Pricebands USD"' ,'"SALES UNITS"' ,'"SALES USD"' ,'"SALES EUR"' ,'"SALES <LC>"' ,'"SV NONSUBS EST. EUR"' ,'"SV NONSUBS EST. USD"' ,'"SV NONSUBS EST. <LC>"']
                                     ,'gfk_tablet'      : ['"FileType"' ,'"Period"' ,'"Quarter"' ,'"Year"' ,'"Country"' ,'"Region"' ,'"ReportingChannel"' ,'"Brand"' ,'"Item"' ,'"DISPLAY SIZE"' ,'"EMBEDDED 3G/4G"' ,'"OPERATING SYST."' ,'"PROCESSOR"' ,'"PROCESSOR BRAND"' ,'"STORAGE IN GB"' ,'"NSP Pricebands EUR"' ,'"NSP Pricebands USD"' ,'"Retail Pricebands EUR"' ,'"Retail Pricebands USD"' ,'"SALES UNITS"' ,'"SALES USD"' ,'"SALES EUR"' ,'"SALES <LC>"' ,'"SV NONSUBS EST. USD"' ,'"SV NONSUBS EST. EUR"' ,'"SV NONSUBS EST. <LC>"']
                                                }

    variables.region_map          =  {'idc_pc'          : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                                     ,'idc_phone'       : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                                     ,'idc_tablet_chnl' : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                                     ,'idc_tablet_seg'  : ['Asia/Pacific (ex. Japan)' ,'Canada', 'Central & Eastern Europe' ,'Japan', 'Latin America' ,'Middle East & Africa', 'USA' ,'Western Europe']
                                     ,'gfk_phone'       : ['ASIA' ,'EUROPE' ,'LATAM' ,'MIDEAST/AFRICA']
                                     ,'gfk_tablet'      : ['ASIA' ,'EUROPE' ,'LATAM' ,'MIDEAST/AFRICA']
                                                }

    variables.country_map         =  {'idc_pc' : ['Australia' ,'Austria' ,'Belgium' ,'Brazil' ,'Canada' ,'Chile' ,'Colombia' ,'Czech Republic' ,'Denmark' ,'Finland' ,'France' ,'Germany' ,'Greece' ,'Hong Kong' ,'Hungary' ,'India' ,'Indonesia' ,'Ireland' ,'Israel' ,'Italy' ,'Japan' ,'Korea' ,'Kuwait' ,'Malaysia' ,'Mexico' ,'Netherlands' ,'Norway' ,'PRC' ,'Philippines' ,'Poland' ,'Portugal' ,'Qatar' ,'Rest of Asia/Pacific' ,'Rest of CEE' ,'Rest of Latin America' ,'Rest of Middle East and Africa' ,'Romania' ,'Russia' ,'Saudi Arabia' ,'Singapore' ,'Slovakia' ,'South Africa' ,'Spain' ,'Sweden' ,'Switzerland' ,'Taiwan' ,'Thailand' ,'Turkey' ,'USA' ,'Ukraine' ,'United Arab Emirates' ,'United Kingdom' ,'Vietnam']
                                     ,'idc_phone'       : []
                                     ,'idc_tablet_chnl' : []
                                     ,'idc_tablet_seg'  : []
                                     ,'gfk_phone'       : []
                                     ,'gfk_tablet'      : []
                                                }

    variables.form_factor_map     =  {'idc_pc' : ['Desktop PC' ,'Portable PC']
                                     ,'idc_phone'       : []
                                     ,'idc_tablet_chnl' : []
                                     ,'idc_tablet_seg'  : []
                                     ,'gfk_phone'       : []
                                     ,'gfk_tablet'      : []
                                                }

    variables.prod_category_map   =  {'idc_pc' : ['All in One PC' ,'Convertible Notebook PC' ,'Mini Notebook PC' ,'Traditional Desktop PC' ,'Traditional Notebook PC' ,'Ultraslim Notebook PC']
                                     ,'idc_phone'       : []
                                     ,'idc_tablet_chnl' : []
                                     ,'idc_tablet_seg'  : []
                                     ,'gfk_phone'       : []
                                     ,'gfk_tablet'      : []
                                                }

    variables.channel_map         =  {'idc_pc' : []
                                     ,'idc_phone'       : []
                                     ,'idc_tablet_chnl' : []
                                     ,'idc_tablet_seg'  : []
                                     ,'gfk_phone'       : []
                                     ,'gfk_tablet'      : []
                                                }

    variables.segment_map         =  {'idc_pc' : ['Consumer' ,'Education' ,'Government' ,'Large Business (500-999)' ,'Medium Business (100-499)' ,'Small Business (10-99)' ,'Small Office (1-9)' ,'Very Large Business (1000+)']
                                     ,'idc_phone'       : []
                                     ,'idc_tablet_chnl' : []
                                     ,'idc_tablet_seg'  : []
                                     ,'gfk_phone'       : []
                                     ,'gfk_tablet'      : []
                                                }

    variables.period_map          =  {'idc_pc' : ['2004Q1' ,'2004Q2' ,'2004Q3' ,'2004Q4' ,'2005Q1' ,'2005Q2' ,'2005Q3' ,'2005Q4' ,'2006Q1' ,'2006Q2' ,'2006Q3' ,'2006Q4' ,'2007Q1' ,'2007Q2' ,'2007Q3' ,'2007Q4' ,'2008Q1' ,'2008Q2' ,'2008Q3' ,'2008Q4' ,'2009Q1' ,'2009Q2' ,'2009Q3' ,'2009Q4' ,'2010Q1' ,'2010Q2' ,'2010Q3' ,'2010Q4' ,'2011Q1' ,'2011Q2' ,'2011Q3' ,'2011Q4' ,'2012Q1' ,'2012Q2' ,'2012Q3' ,'2012Q4' ,'2013Q1' ,'2013Q2' ,'2013Q3' ,'2013Q4' ,'2014Q1' ,'2014Q2' ,'2014Q3']
                                     ,'idc_phone'       : []
                                     ,'idc_tablet_chnl' : []
                                     ,'idc_tablet_seg'  : []
                                     ,'gfk_phone'       : []
                                     ,'gfk_tablet'      : []
                                                }

    variables.price_band_map      =  {'idc_pc' : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                                     ,'idc_phone'       : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                                     ,'idc_tablet_chnl' : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                                     ,'idc_tablet_seg'  : ['01: $0<$50' ,'02: $50<$100' ,'03: $100<$150' ,'04: $150<$200' ,'05: $200<$250' ,'06: $250<$300' ,'07: $300<$350' ,'08: $350<$400' ,'09: $400<$450' ,'10: $450<$500' ,'11: $500<$550' ,'12: $550<$600' ,'13: $600<$650' ,'14: $650<$700' ,'15: $700<$800' ,'16: $800<$900' ,'17: $900<$1K' ,'18: $1K<$1.1K' ,'19: $1.1K<$1.2K' ,'20: $1.2K<$1.3K' ,'21: $1.3K<$1.4K' ,'22: $1.4K<$1.5K' ,'23: $1.5K<$1.6K' ,'24: $1.6K<$1.7K' ,'25: $1.7K<$1.8K' ,'26: $1.8K<$1.9K' ,'27: $1.9K<$2K' ,'28: $2K<$2.5K' ,'29: $2.5K<$3K' ,'30: $3K<$5K' ,'31: $5K+']
                                     ,'gfk_phone'       : ['0 < 100 USD' ,'100 < 200 USD' ,'200 < 300 USD' ,'300 < 400 USD' ,'400 < 500 USD' ,'500 < 600 USD' ,'600 < 700 USD' ,'>= 700 USD','TOTAL']
                                     ,'gfk_tablet'      : ['0 < 100 USD' ,'100 < 200 USD' ,'200 < 300 USD' ,'300 < 400 USD' ,'400 < 500 USD' ,'500 < 600 USD' ,'600 < 700 USD' ,'>= 700 USD','TOTAL']
                                                }

    
if __name__ == '__main__':
    main()


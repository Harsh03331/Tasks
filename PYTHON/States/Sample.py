import re
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import configparser
import pandas as pd
import dateparser
from dateutil import parser as dparser
import datetime
import time
from nameparser import HumanName
from selenium.webdriver.support.ui import Select

data = []
# ... (your existing import statements and functions) ...
base_url					= 'https://uk.eu-supply.com'
block_match 				= '<tr>\s*<td>[\w\W]*?<\/tr>'
sub_url_regex				= '<\/span>\s*<a\s*href="([^>]*?)"[^>]*?>'
sourcecw 					= 'Contrax Weekly'
authorityname 				= 'Buyer:[\w\W]*?<br \/>\s*([^>]*?)\s*<br \/>'
origin 						= 'UK/Defence'
sector 						= 'UK Emergency Services'
authoritydept 				= 'None'
country_codes 				= 'GB'
country 					= 'GB'
web_source 					= 'Bluelight (2): Emergency Services E-Tendering - EU Supply'
industry_sector 			= 'Other'
pubflagcw 					= 'None'
title 						= '<\/span>\s*<a\s*href="[^>]*?"[^>]*?>([^>]*?)<\/a>'
authorityaddress1 			= 'Buyer[\w\W]*?<br \/>\s*[^>]*?\s*<br \/>\s*([^>]*?)\s*<br \/>'
authorityaddress2 			= 'None'
authorityaddress3 			= 'None'
authoritytown 				= 'Buyer[\w\W]*?<br \/>\s*[\w\W]*?<br \/>[\w\W]*?<br \/>[^>]*?<br \/>\s*([^>]*?)\s*<br \/>'
authoritycounty 			= 'None'
authoritypostcode 			= 'Buyer[\w\W]*?<br \/>\s*[\w\W]*?<br \/>[\w\W]*?<br \/>\s*([^>]*?)\s*<br \/>'
authoritytelephone 			= 'None'
authorityfax 				= 'None'
authorityemail 				= 'None'
authoritywebaddress 		= 'Contact:[\w\W]*?<a\s*href=[\w\W]*?>(http[^>]*?)<\/a>'
authorityprofileurl 		= 'None' 
authoritycontactname 		= 'Contact:[\w\W]*?<p>\s*([^>]*?)\s*<'
authorityposition 			= 'None'
earliestdate 				= 'None'
cpv_code 					= '>\s*CPV\s*codes\S([\w\W]*?)<\/p>\s*<\/div>'
origpublicationdate 		= '<span[\w\W]*?<td>\s*[\w\W]*?">\s*([^>]*?)\s*<\/div>'
proofed 					= 'None'
description 				= '<p class="ctm-multi-line">([\w\W]*?)<\/p>'
location 					= 'None'
authority_reference 		= '<td>\s*<div data-toggle="tooltip"[^>]*?>\s*([^>]*?)\s*<\/div>\s*<\/td>\s*<td>\s*<span'
contract_start_date 		= 'None'
contract_end_date 			= 'None'
value 						= 'None'
value2 						= 'None'
value3						= 'None'
currency 					= 'None'
amount 						= 'None'
amount_min 					= 'None'
amount_max 					= 'None'
deadline_description 		= 'Response deadline'
deadline_date 				= '<div class="ctm-content-label">Response deadline[\w\W]*?<p>(\d{2,}\/\d{2,}\/\d{3,})\s*[^>]*?<\/p>'
deadline_time 				= '<div class="ctm-content-label">Response deadline[\w\W]*?<p>\d{2,}\/\d{2,}\/\d{3,}\s*([^>]*?)<\/p>'
sent_to 					= 'None'
other_information			= 'None'
nuts_code 					= 'None'
award_procedure             = '<span[^>]*?>[\w\W]*?<\/div>[\w\W]*?<\/div>[\w\W]*?">\s*([^>]*?)\s*<\/div>'
source_name 				= 'Bluelight (2): Emergency Services E-Tendering - EU Supply'
contract_type               = '<div[^>]*?>Type of contract[\w\W]*?\s*<p>([^>]*?)<\/p>'
NEXT_PAGE_REGEX				= 'None'

def reg_clean(desc):
    desc = desc.replace('\r', '').replace('\n', '')
    desc = desc.replace('&#160;', '')
    desc =  desc.replace("'","''")
    desc = desc.replace('\s+\s+', ' ')
    desc = re.sub(r'<[^<]*?>', ' ', str(desc))
    desc = re.sub(r"&#39;","''", str(desc))
    desc = re.sub(r'\r\n', '', str(desc), re.I)
    desc = re.sub(r"\\r\\n", '', str(desc), re.I)
    desc = re.sub(r'\t', " ", desc, re.I)
    desc = re.sub(r'\s\s+', " ", desc, re.I)
    desc = re.sub(r"^\s+\s*", "", desc, re.I)
    desc = re.sub(r"\s+\s*$", "", desc, re.I)
    desc = re.sub(r"\&rsquo\;", "''", desc, re.I)
    desc = re.sub(r"\&ndash\;", "-", desc, re.I)
    desc = re.sub(r"&nbsp;"," ",desc, re.I)
    desc = re.sub(r"&amp;","",desc, re.I)
    desc = desc.replace('&nbsp;','')
    desc = desc.replace('&quot;','')
    desc = desc.replace('&lt;p&gt;','')
    desc = desc.replace('&#193;','')

    return desc

def regex_match(regex,content):
    if regex != "None":
        value = re.findall(regex,str(content))
        if len(value) == 0:
            value1 = ""
        else:
            value1 = reg_clean(value[0])
    else:
        value1 = ""
    
    return (value1)

def DateFormat(Input):
    try:
#         print ("DATE Before Format :: ",Input)
        dt=dparser.parse(Input,fuzzy=True,dayfirst = True)
#         FormattedDate = (dt.strftime('%Y-%m-%d %H:%M:%S'))
        FormattedDate = (dt.strftime('%d-%m-%Y'))
    except Exception as e:
        dt = dateparser.parse(time.asctime())
        FormattedDate = (dt.strftime('%d-%m-%Y'))
#         FormattedDate = (dt.strftime('%Y-%m-%d %H:%M:%S'))
    return (FormattedDate)

def timeFormat(Input):
    Formattedtime = Input.strip()
    
    # Regex pattern to match hours and minutes with optional AM or PM suffix
    time1 = re.findall('(\d{1,2})(?:\:|\.)(\d{2})?\s*(?:am|AM|pm|PM)?', Formattedtime)
    
    if time1:
        hour, minute = int(time1[0][0]), int(time1[0][1]) if time1[0][1] else 0
        
        # Convert to 24-hour format based on AM or PM
        if 'pm' in Formattedtime.lower() and hour < 12:
            hour += 12
        elif 'am' in Formattedtime.lower() and hour == 12:
            hour = 0
            
        # Format the time as HH:MM:SS
        Formattedtime = f"{hour:02d}:{minute:02d}:00"
    
    return Formattedtime

def AmountFormat(amount):
    # Check if "million" is present in the string
    if 'million' in amount.lower():
        # Remove non-numeric characters (except for periods and commas)
        cleaned_amount = re.sub(r'[^0-9.,]', '', amount)

        # Replace commas with empty strings and convert to float
        formatted_amount = float(cleaned_amount.replace(',', ''))

        # Multiply by a million to get the final value
        formatted_amount *= 1000000
    else:
        # If "million" is not present, directly convert to float
        formatted_amount = float(re.sub(r'[^0-9.,]', '', amount).replace(',', ''))

    # Convert to integer if the value has no decimal places
    if formatted_amount.is_integer():
        formatted_amount = int(formatted_amount)

    return formatted_amount

def regex_checking_updating(content,tender_url,awardProcedure,authorityreference1,title1,origpublicationdate_formatted):
    
    url1 = tender_url
    
    contract_Type = regex_match(contract_type, str(content))
    if 'Supplies' in contract_Type:
        contractType = 'Contract type: Supply contract'
    elif 'Works' in contract_Type:
        contractType = 'Contract type: Public works contract'
    elif 'Services' in contract_Type:
        contractType = 'Contract type: Service contract'
    else:
        contractType = ''
    
    authority_contact = regex_match(authoritycontactname,str(content))
    if authority_contact:
        name = HumanName(authority_contact)
        authority_contactfirstname = name.first
        authority_contactlastname = name.last
        authority_contactsalutation = name.title
    else:
        authority_contactfirstname = ''
        authority_contactlastname = ''
        authority_contactsalutation = ''
    
    authority_webaddress = regex_match(authoritywebaddress,str(content))
    authority_profileurl = regex_match(authorityprofileurl,str(content))
    authority_position = regex_match(authorityposition,str(content))   
    authority_dept = regex_match(authoritydept, str(content))
   
    
    deadline_date1 = regex_match(deadline_date, str(content))
    if deadline_date1:
        deadline_date_formatted = DateFormat(deadline_date1)
        deadline_description1 = regex_match(deadline_description, str(content))
        if deadline_description != "None":
            if deadline_description1:
                deadline_description2 = deadline_description1
            else:
                deadline_description2 = deadline_description
    else:
        deadline_date_formatted = ""
        deadline_description2 = ""
   
    if deadline_time != "None":
        deadline_time_re = re.findall(deadline_time,str(content))
        if len(deadline_time_re) == 0:
            deadline_time1 = ""
        else:
            deadline_time1 = timeFormat(deadline_time_re[0])
    else:
        deadline_time1 = ""

    if cpv_code != 'None':
        cpv_codes = regex_match(cpv_code, str(content))
        cpvpattern = re.sub(r'\-\d\s*\D+', ',', cpv_codes)
        cpvcode = ',\t'.join(filter(None, cpvpattern.split(',')))

    pubflag = regex_match(pubflagcw, str(content))

    proofed1 = regex_match(proofed, str(content))

    location1 = regex_match(location, str(content))

    sourcename = regex_match(source_name, str(content))

    description1 = regex_match(description,str(content))

    earliest_date = regex_match(earliestdate, str(content))
    contract_startdate = regex_match(contract_start_date, str(content))
    contract_enddate = regex_match(contract_end_date, str(content))


    if earliest_date:
        earliest_date_formatted = DateFormat(earliest_date)
    else:
        earliest_date_formatted = ""

    if contract_startdate:
        contract_startdate_formatted = DateFormat(contract_startdate)
    else:
        contract_startdate_formatted = ""

    if contract_enddate:
        contract_enddate_formatted = DateFormat(contract_enddate)
    else:
        contract_enddate_formatted = ""

    if other_information != 'None':
        otherinfo = regex_match(other_information, str(content))
    else:
        otherinfo = tender_url

    if sent_to == "None":
        sentto = "For further information regarding the above contract notice please visit:" + tender_url


    values = regex_match(value, str(content))
    print('Values:',values)

    currency1 = ''
    amount1 = ''    
    if amount != 'None':
        amount2 = regex_match(amount, str(content))
        if amount2:
            amount1 = AmountFormat(amount2)
            currency1 = currency
        if 'N/A' in amount2:
            amount1 = ''
            currency1 = ''
                
        if amount2.endswith('.'):
            amount1 = AmountFormat(amount2[:-1])
            currency1 = currency
    else:
        amount1 = ''
        currency1 = ''
    
    amountmin = regex_match(amount_min, str(content))
    
    amountmax = regex_match(amount_max, str(content))
    
#     viewprofile = regex_match(r'<a\s*href="([^>]*?)"[^>]*?>\s*View', content)
#     if viewprofile:
#         profileurl = base_url + viewprofile
#         print('profileurl : ', profileurl)
#         profilepage = requests.get(profileurl)
#         profilecontent = profilepage.content.decode('utf-8', errors='ignore')
        
    authority = regex_match(authorityname,str(content))
    authority_address1 = regex_match(authorityaddress1,str(content))
    authority_address2 = regex_match(authorityaddress2,str(content))
    authority_address3 = regex_match(authorityaddress3,str(content))
    authority_town = regex_match(authoritytown,str(content))
    authority_county = regex_match(authoritycounty,str(content))
    authority_PostCode = regex_match(authoritypostcode,str(content))
    authority_fax = regex_match(authorityfax,str(content))
    authorityemail1 = regex_match(authorityemail,str(content))

    authority_telephone = regex_match(authoritytelephone,str(content))
    prefix = r"\+353"
    authority_telephone1 = re.sub(prefix,'00353',authority_telephone)
        
        
    nutscode = regex_match(nuts_code,str(content))
    highvalue = ''
    site = ''
    frameworkAgreement = ''
    nc = ''
    no_of_months = ''

    data.append({'title':title1,'origin':origin,'authorityName':authority,'noticeSector':sector,'cy':country,
                 'authorityAddress1':authority_address1,'sourceURL':source_name,'authorityAddress2':authority_address2,
                 'authorityAddress3':authority_address3,'pubFlagCW':pubflag,'authorityTown':authority_town,'authorityCounty':authority_county,
                 'authorityPostcode':authority_PostCode,'authorityCountry':country_codes,'authorityTelephone':authority_telephone1,
                 'authorityFax':authority_fax,'authorityEmail':authorityemail1,'authorityWebAddress':authority_webaddress,'authorityProfileURL':authority_profileurl,
                 'authorityContactSalutation':authority_contactsalutation,'authorityContactFirstName':authority_contactfirstname,
                 'authorityContactLastName':authority_contactlastname,'authorityPosition':authority_position,'awardProcedure':awardProcedure,
                 'contractType':contractType,'earliestDate':earliest_date_formatted,'cpvNos':cpvcode,'nuts':nutscode,'Industry_Sector':industry_sector,
                 'origPublicationDate':origpublicationdate_formatted,'description':description1,'proofed':proofed1,'site':site,'authorityRefNo':authorityreference1,
                 'no_of_months':no_of_months,'contract_start_date':contract_startdate_formatted,'contract_end_date':contract_enddate_formatted,'value':values,
                 'currency':currency1,'amount':amount1,'amount_min':amountmin,'amount_max':amountmax,'cw_RAdeadline':deadline_description2,
                 'd_RA':deadline_date_formatted,'d_RAtime':deadline_time1,'d_RApost':sentto,'otherInformation':otherinfo})

def main():
    service = Service(executable_path=r"C:\Users\VC\Downloads\chromedriver-win64\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the initial URL
#     org_url = 'https://uk.eu-supply.com/ctm/supplier/publictenders?B=BLUELIGHT'
    url = 'https://uk.eu-supply.com/ctm/Supplier/PublicTenders'
    driver.get(url)
    dropdown_element = driver.find_element("id",'SearchFilter_BrandingCode')
    select = Select(dropdown_element)
    select.select_by_visible_text('All')
    search = driver.find_element("id",'search').click()
#     print(driver.page_source)
    wait = WebDriverWait(driver, 10)

    # Set the total number of pages you want to scrape
    total_pages = 1
    
    main_content = driver.page_source
    for page_num in range(1, total_pages + 1):
        blockmatch = re.findall(block_match, main_content)
        for i in blockmatch:
#             print('Block --- ',i)
            title1 = regex_match(title, i)
           

            authorityreference = regex_match(authority_reference, i)
            authorityreference1 = authorityreference

            award_Procedure = regex_match(award_procedure, i)
            award_Procedure1 = re.sub(r'\d+\.\s*', '', award_Procedure)
            awardprocedure = re.findall(r'Open Procedure',award_Procedure1)
            if awardprocedure:
                awardProcedure = 'Open'
            else:
                awardProcedure = award_Procedure1

            origpublicationdate1 = regex_match(origpublicationdate, i)
            if origpublicationdate1:
                origpublicationdate_formatted = DateFormat(origpublicationdate1)
            else:
                origpublicationdate_formatted = ""
            
            sub_urls = re.findall(sub_url_regex, i)
            for j in sub_urls:
                if not j.startswith("http"):
                    tender_url = base_url + j
                else:
                    tender_url = j
#                 print('Url: ', tender_url)
                    
    #  ----------------getting content from tender urls--------------
                r1 = requests.get(tender_url)
                content = r1.content.decode('utf-8', errors='ignore')

                rftpage = re.findall(r'<a\s*id="showTenderDetails[^>]*?href="([^>]*?)"[^>]*?>', content)
                if rftpage:
                    url = base_url + rftpage[0]
                    rftdetailspage = requests.get(url)
                    content = rftdetailspage.content.decode('utf-8', errors='ignore')
                else:
                    content = content
                exclude_text = ['(Contracts Finder)','(FTS)']    
                if not any(keyword in content for keyword in exclude_text):
                    print('Title : ', title1)
                    print('URL : ', tender_url)
                    regex_checking_updating(content, tender_url, awardProcedure,authorityreference1,title1,origpublicationdate_formatted)

#     -----------Pagination-----------
        wait = WebDriverWait(driver, 30)
        link_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.pager-action.ctm-icon-link')))
        print(link_element)
        link_element.click()
        time.sleep(30)
        main_content = driver.page_source

    driver.quit()

#     # Create a pandas DataFrame from the collected data
main()
datadf = pd.DataFrame(data)

# # Call the main function to start scraping
# if __name__ == "__main__":
#     main()

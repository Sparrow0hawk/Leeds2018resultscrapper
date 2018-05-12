
# # text scrape 2018 local election results into a panda dataframe
# # with csv output

# In[11]:

# import library for querying website
import pandas as pd
import os
import urllib2
import requests
import html5lib
from bs4 import BeautifulSoup
from io import StringIO


# reformat initial dict
links = {"Ward" : ["Adel and Wharfedale","Alwoodley","Ardsley and Robin Hood","Armley","Beeston and Holbeck",
                   "Bramley and Stanningley","Burmantofts and Richmond Hill","Calverley and Farsley","Chapel Allerton",
                  "Cross Gates and Whinmoor","Farnley and Wortley","Garforth and Swillington","Gipton and Harehills",
                  "Guiseley and Rawdon","Harewood", "Headingley and Hyde Park","Horsforth", "Hunslet and Riverside",
                  "Killingbeck and Seacroft","Kippax and Methley", "Kirkstall","Little London and Woodhouse", "Middleton Park",
                  "Moortown","Morley North","Morley South","Otley and Yeadon","Pudsey","Rothwell","Roundhay","Temple Newsam",
                  "Weetwood","Wetherby"],
         "Link" : ["https://www.leeds.gov.uk/your-council/elections/election-results?ward=Adel%20and%20Wharfedale",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Alwoodley",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Ardsley%20and%20Robin%20Hood",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Armley",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Beeston%20and%20Holbeck",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Bramley%20and%20Stanningley",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Burmantofts%20and%20Richmond%20Hill",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Calverley%20and%20Farsley",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Chapel%20Allerton",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Cross%20Gates%20and%20Whinmoor",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Farnley%20and%20Wortley",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Garforth%20and%20Swillington",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Gipton%20and%20Harehills",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Guiseley%20and%20Rawdon",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Harewood",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Headingley%20and%20Hyde%20Park",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Horsforth",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Hunslet%20and%20Riverside",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Killingbeck%20and%20Seacroft",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Kippax%20and%20Methley",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Kirkstall",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Little%20London%20and%20Woodhouse",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Middleton%20Park",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Moortown",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Morley%20North",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Morley%20South",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Otley%20and%20Yeadon",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Pudsey",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Rothwell",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Roundhay",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Temple%20Newsam",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Weetwood",
                 "https://www.leeds.gov.uk/your-council/elections/election-results?ward=Wetherby"]}

# use the .from_records and define indexes
tbl_1 = pd.DataFrame.from_dict(links)

# correct table!
tbl_1.head()


# -------------------------------------------------
# Combined scrapper for data and ward, turnout, electorate
# -------------------------------------------------

# In[9]:

# query page and return html to variable page

def get_data(df):
    
    df_y = []
    
    for index, row in df.iterrows():
        # identify and pull out results table as a pandas dataframe and append to list
        # of dataframe for future concat
        df = pd.read_html(row['Link'],header=0)[1]
        
        # identify and pull out turnout, ward and electorate 
        # append to each iterated dataframe before append to list of dataframes
        page = urllib2.urlopen(row["Link"])
        soup = BeautifulSoup(page,'html.parser')
        turn_1 = soup.find(id="ctl00_ctl46_g_83fe6653_6a71_4ec6_b347_267539a339e8")
        turn_1 = turn_1.text.strip()
        turn_1 = turn_1[46:125]
        turn_1 = turn_1.split(" ")
        # get turnout
        for i in turn_1:
            if i == "%":  
                break
            else:
                z = ''
                z += i
        df["Turnout"] = z
        j = ""
        # get total ward
        for i in turn_1:
            if i == "Electorate":  
                break
            else:
               
                j += " "+i
        df['Ward'] = j

        # get total electorate
        for i in turn_1:
            if i == "Turnout":  
                break
            else:
                b = ""
                b += i
        df['Electorate'] = b
                
        # append dataframe to list of dataframes
        df_y.append(df)
        
    df_y = pd.concat(df_y,axis=0, ignore_index=True)
    
    return df_y

x = get_tables(tbl_1)


# In[13]:

x.head()

path = "#enter path"

x.to_csv(os.path.join(path,"2018_results.csv"))


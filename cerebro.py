
from bs4 import BeautifulSoup
import httpx
import re
from time import sleep
import pandas as pd
import traceback
import numpy as np
import re

def get_paperinfo(paper_url):

  #download the page
  response=httpx.get(paper_url)

  # check successful response
  if response.status_code != 200:
    print('Status code:', response.status_code)
    #raise Exception('Failed to fetch web page ')
    resp = False
    paper_doc = ""
  else:
    resp = True
    print("Got it!")
    #parse using beautiful soup
    paper_doc = BeautifulSoup(response.text,'html.parser')

  return paper_doc, resp

# this function for the extracting information of the tags
def get_tags(doc):
  paper_tag = doc.select('[data-lid]')
  cite_tag = doc.select('[title=Cite] + a')
  link_tag = doc.find_all('h3',{"class" : "gs_rt"})
  author_tag = doc.find_all("div", {"class": "gs_a"})

  return paper_tag,cite_tag,link_tag,author_tag

# it will return the title of the paper
def get_papertitle(paper_tag):
  
  paper_names = []
  
  for tag in paper_tag:
    paper_names.append(tag.select('h3')[0].get_text().replace("[HTML][HTML] ","").replace("[PDF][PDF] ",""))

  return paper_names


# it will return the number of citation of the paper
def get_citecount(cite_tag):
  cite_count = []
  for i in cite_tag:
    cite = i.text
    if i is None or cite is None:  # if paper has no citatation then consider 0
      cite_count.append(0)
    else:
      tmp = re.search(r'\d+', cite) # its handle the None type object error and re use to remove the string " cited by " and return only integer value
      if tmp is None :
        cite_count.append(0)
      else :
        cite_count.append(int(tmp.group()))

  return cite_count

# function for the getting link information
def get_link(link_tag):

  links = []

  for i in range(len(link_tag)) :
    links.append(link_tag[i].a['href']) 

  return links 

# function for the getting author , year and publication information
def get_author_year_publi_info(authors_tag):
  years = []
  publication = []
  authors = []
  for i in range(len(authors_tag)):
      authortag_text = (authors_tag[i].text).split()
      
      publication.append(authortag_text[-1])

      year = re.search(r'\d+', authors_tag[i].text)
      if year:
        year = int(year.group())
        if year < 1950 and year > 2050:
           year = np.nan
        else:
           year = str(year)
      else:
         year = np.nan
      years.append(year)
      
      author = authortag_text[0] + ' ' + re.sub(',','', authortag_text[1])
      authors.append(author)
  
  return years , publication, authors

# creating final repository
paper_repos_dict = {
                    'Paper Title' : [],
                    'Year' : [],
                    'Author' : [],
                    'Citation' : [],
                    'Publication' : [],
                    'Url of paper' : [] }

# adding information in repository
def add_in_paper_repo(papername,year,author,cite,publi,link):
  paper_repos_dict['Paper Title'].extend(papername)
  paper_repos_dict['Year'].extend(year)
  paper_repos_dict['Author'].extend(author)
  paper_repos_dict['Citation'].extend(cite)
  paper_repos_dict['Publication'].extend(publi)
  paper_repos_dict['Url of paper'].extend(link)

  return pd.DataFrame(paper_repos_dict)

def ask(query, from_y = None, to_y = None,page_limits=None):
    
    df = pd.DataFrame(columns = ['Year', 'Title', 'Author','Publication'])
    
    if not page_limits:
        page_limits = 100

    if from_y:
       query += "&as_ylo=" + str(from_y)

    if to_y:
       query += "&as_yhi=" + str(to_y)

    try:
        for i in range (0,10*page_limits,10):
            print("Page",int(i/10+1))
            # get url for the each page
            url = "https://scholar.google.com/scholar?start={}&q=".format(i) + query + "&hl=en&as_sdt=0,5"
            
            #print(url)
            # function for the get content of each page
            doc,resp = get_paperinfo(url)
            if not resp:
                print("not responding anymore")
                break

            # function for the collecting tags
            paper_tag,cite_tag,link_tag,author_tag = get_tags(doc)
            
            # paper title from each page
            papername = get_papertitle(paper_tag)

            # year , author , publication of the paper
            year , publication , author = get_author_year_publi_info(author_tag)

            # url of the paper (Some errors when: 'NoneType' object is not subscriptable)
            #link = get_link(link_tag)

            # add in paper repo dict
            #print(len(papername),len(year),len(author),len(publication))

            
            data = {'Year': year, 'Title': papername, 'Author': author,'Publication': publication}
            
            #print(data)

            new_entries = pd.DataFrame(data=data)
            print(new_entries)

            df = pd.concat([df,new_entries],ignore_index=True)

            #final = add_in_paper_repo(papername,year,author,cite,publication,link)
            #print(final)
            # use sleep to avoid status code 429
            sleep(30)
    except Exception: 
       traceback.print_exc()
       return df
        
    return df


def cjk_detect(texts):
    # korean
    if re.search("[\uac00-\ud7a3]", texts):
        return "ko"
    # japanese
    if re.search("[\u3040-\u30ff]", texts):
        return "ja"
    # chinese
    if re.search("[\u4e00-\u9FFF]", texts):
        return "zh"
    return None

def load(file):
   return pd.read_csv(file)

def clean_results(df):
   df = df.drop_duplicates()
   df = df[~df.Title.str.contains("CITATION")]
   return df

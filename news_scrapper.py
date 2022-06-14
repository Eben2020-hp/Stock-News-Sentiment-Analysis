'''
    We need to create a scrapper that can get for us the Stock News of the whole week. 
    For this first we will be extracting all the news articles.
    We will be taking all the contents inside each link (Thus we need to click each article and extract the content).
    We only need articles that go back till one week.

    We know that BeautifulSoup is n HTML Parser. So we will integrate Selenium inorder to navigate through pages.

'''

## Scrapper Imports
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()            ### Checks if the chromedriver is up-to-date and installs the updates driver if needed. 

## Python module used for extracting and parsing newspaper articles
from newspaper import Article


## Data Analysis
import pandas as pd
import time

## Summarizer using Spacy  ---> Another File
from Summarizer import summarize


driver = webdriver.Chrome()

Company_Of_Interest = input('Enter the company of interest: ').lower().replace(" " , "+")
url = [f'https://news.google.com/search?q={Company_Of_Interest}+stock&hl=en-IN&gl=IN&ceid=IN%3Aen']

df = pd.DataFrame(columns= ['Article_Name', 'Article_Headline', 'Link', 'Content', 'Summary'])

def main():
    global soup
    driver.get(url[-1])
    pageHTML = driver.page_source

    soup = BeautifulSoup(pageHTML, 'lxml')
    article = soup.find_all('div', class_='NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc')

    for data in article: 
        post_time = data.find('time', class_='WW6dff uQIVzc Sksgp').text
        if ('hour' in post_time) or ('hours' in post_time) or ('day' in post_time) or ('days' in post_time) or ('week' in post_time) and ('weeks' not in post_time):
            article_name = data.find('div', class_='SVJrMe').a.text
            article_headline = data.find('h3', class_='ipQwMb ekueJc RD0gLb').text
            link = data.find('a', class_= 'VDXfz', href=True)['href']
            link = 'https://news.google.com'+link

            try:
                news = Article(link, language= 'en')
                news.download()
                news.parse()
                article_content = news.text             ### Helps obtain all the text in the given news article.
                summary = summarize(news.text, 0.20)
            except Exception as e:
                pass
            else:
                df.loc[len(df.index)] = [article_name, article_headline, link, article_content, " ".join(summary.split())]

        else:
            pass


main()
print(df)
df.to_csv('GoogleStockNews.csv', index= False)
driver.quit()



"""
    REFERENCE:
    1. https://stackoverflow.com/questions/56106040/unable-to-scrape-google-news-heading-via-their-class    ---> To be done when using just BeautifulSoup.
    2. https://youtu.be/AEOQiUYNj3E   ---> Newspaper Package
    3. pip install newspaper3k  
    4. pip install chromedriver-autoinstaller ---> https://pypi.org/project/chromedriver-autoinstaller/
    5. https://www.activestate.com/blog/how-to-do-text-summarization-with-python/  ---> Article on getting the Text


""" 
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.imdb.com/chart/top'

try:
    page = requests.get(URL)
    page.raise_for_status()
    time.sleep(2)

    soup = BeautifulSoup(page.content, 'lxml')
    movies = soup.find('tbody', class_="lister-list").find_all('tr')
    
    movie_rank_list = []
    movie_name_list = []
    release_date_list = []
    imdb_rating_list = []

    for movie in movies:
        movie_rank = movie.find('td', class_="titleColumn").text.strip().split(".")[0]
        movie_rank_list.append(movie_rank)
        movie_name = movie.find('td', class_="titleColumn").a.text
        movie_name_list.append(movie_name)
        release_date = movie.find('td', class_="titleColumn").span.text.strip("()")
        release_date_list.append(release_date)
        movie_rating = movie.find('td', class_="ratingColumn imdbRating").strong.text
        imdb_rating_list.append(movie_rating)
 
    movie_details = {
        "Rank": movie_rank_list,
        "Name": movie_name_list,
        "Year": release_date_list,
        "Rating": imdb_rating_list
    }

    df = pd.DataFrame(movie_details)
    excel = df.to_excel('imdb_top_250_movies.xlsx')

except Exception as e:
    print(e)



import pandas as pd
import requests
from time import time, sleep
from random import randint
from bs4 import BeautifulSoup

# create empty DataFrame to save dataset
movies_df = pd.DataFrame()

# i want to get movies from 1994-2020
for year in range(1994, 2021):
    # imdb has arg start which takes number of movies to start from
    # by default it starts at 1 and increments by 50
    # i will be getting first 200 movies in list per year
    for start in range(1, 201, 50):

        url = f"https://www.imdb.com/search/title/?release_date={year}&sort=num_votes,desc&start={start}&ref_=adv_nxt"
        response = requests.get(url)
        # only parse data if response is 200
        if response.status_code == 200:

            # create object from BeautifulSoup with response text using lxml parser
            soup = BeautifulSoup(response.text, 'lxml')

            # get all movies in single page
            cards = soup.find_all("div", class_="lister-item mode-advanced")

            for movie in cards:

                # data set contain movies and tvshows, i want to get movies only
                # only movies has the metascore attribute so will filter by it
                meta_score_attr = movie.find("div", "inline-block ratings-metascore")

                if meta_score_attr is not None:
                    # there is only one h3 tag with title
                    title = movie.h3.a.text

                    # movie parental rating
                    rated = movie.find("span", class_="certificate").text \
                        if movie.find("span", class_="certificate") is not None else None

                    genre = movie.find("span", class_="genre").text

                    runtime = movie.find("span", class_="runtime").text

                    director = movie.find("p", class_="").text.strip().strip("\n").split('|')[0].strip("Director:") \
                        .strip("\n")

                    stars = [star.strip(" \n") for star in
                             (movie.find("p", class_="").text.strip().strip("\n").split('|')[1].strip().strip("Stars:")
                              .split(","))]

                    rating = float(movie.find("div", class_="inline-block ratings-imdb-rating").strong.text)

                    about = movie.find_all("p", class_="text-muted")[1].text

                    votes_count = movie.find("p", class_="sort-num_votes-visible").find_all("span")[1]['data-value']

                    gross = movie.find("p", class_="sort-num_votes-visible").find_all("span")[4]['data-value']

                    movies_df = movies_df.append({
                        "title": title,
                        "rating_type": rated,
                        "genre": genre,
                        "runtime": runtime,
                        "about": about,
                        "director": director,
                        "stars": stars,
                        "rating": rating,
                        "votes_count": votes_count,
                        "gross": gross

                    }, ignore_index=True)
                    sleep(randint(1, 4))


movies_df.to_csv('movies_dataset.csv', index=False)
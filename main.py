import pandas as pd
from flask import Flask, render_template
from movies import weighted_ranked_movies, top_50_movies_weighted_score, get_movies_by_genre

app = Flask(__name__)

############################################################################################################
# Data Sources
############################################################################################################

# Raw List of 4800+ Movies
movies_df_raw = pd.read_csv("Movies_Data/movies.csv")

# Ordered List of Movies using Weighted Ranking Formula
weighted_movies_df = weighted_ranked_movies(movies_df_raw)

# Top 50 Movies based on Weighted Score
top_fifty_movies = top_50_movies_weighted_score(weighted_movies_df)


############################################################################################################
# API Configuration
############################################################################################################


# Home Page should pull in URL Templates and top 50 Movies by Rating
@app.route("/")
def home():
    return render_template("home.html", data=top_fifty_movies.to_html())


@app.route("/api/v1/<movie_name>")
def get_movie_details(movie_name):
    df = weighted_movies_df

    # Create a new DF to store only movies that match the year specified in the URL
    movie_df = df[df["title"] == str(movie_name)]
    # Convert the DataFrame to a list of dictionaries
    records = movie_df.to_dict(orient="records")

    # Figure out how to maintain order of columns. Json output is ordering alphabetically
    return records


@app.route("/api/v1/year/<year>")
def movies_by_year(year):
    df = weighted_movies_df

    # Extract the year and save it as a new column called release_year
    df["release_year"] = df["release_date"].astype(str).str.split('-').str[0]

    # Create a new DF to store only movies that match the year specified in the URL
    year_df = df[df["release_year"] == str(year)]
    year_df = year_df[["title", "release_year", "tagline", "runtime", "vote_average"]]

    # Convert the DataFrame to a list of dictionaries
    records = year_df.to_dict(orient="records")

    # Figure out how to maintain order of columns. Json output is ordering alphabetically

    return records





@app.route("/api/v1/genre/<genre>")
def movies_by_genre(genre):
    df = get_movies_by_genre(weighted_movies_df, genre)

    genre_df = df[["title", "release_date", "tagline", "runtime", "vote_average", "genres"]]

    # Convert the DataFrame to a list of dictionaries
    records = genre_df.to_dict(orient="records")

    return records


if __name__ == "__main__":
    app.run(debug=True)


import json


def weighted_rating(v, m, R, C):
    """
    Calculate Weighted Movie Rating
    WR = (v ÷ (v+m)) × R + (m ÷ (v+m)) × C
    """
    return ((v / (v + m)) * R) + ((m / (v + m)) * C)


def weighted_ranked_movies(df):
    m = df['vote_count'].quantile(0.9)
    C = df["vote_average"].mean()

    # Calculate weighted ratings using a lambda function
    df["weighted_rating"] = df.apply(lambda row: weighted_rating(row["vote_count"], m, row["vote_average"], C), axis=1)

    # Rank the movies based on weighted ratings
    df["rank"] = df["weighted_rating"].rank(ascending=False)

    # Filter movies with vote_count greater than or equal to the threshold (m)
    weighted_movies_data_frame = df[df["vote_count"] >= m].sort_values(by="rank", ascending=True)

    return weighted_movies_data_frame


def top_50_movies_weighted_score(df):
    weighted_df = weighted_ranked_movies(df)

    movies_top_50_df = weighted_df[
        ["title", "release_date", "tagline", "runtime", "original_language", "vote_average", "vote_count", "rank"]]

    movies_top_50_df.loc[:, "runtime"] = movies_top_50_df["runtime"].divide(60).round(2)

    movies_top_50_df = movies_top_50_df.sort_values(by="rank", ascending=True).head(50)

    return movies_top_50_df


def get_movies_by_genre(df, genre_name):
    # Define an inner function to check if the specified genre name exists in the genres list string of a movie.
    def is_genre_match(genre_list_str):
        # Attempt to load the genre list string as JSON and return True if the genre_name is found in any of the genre dictionaries.
        try:
            genres = json.loads(genre_list_str)
            return any(genre['name'] == genre_name for genre in genres)
        # Return False if there is an error decoding the JSON, indicating the genre is not found or the data is malformed.
        except json.JSONDecodeError:
            return False

    # Apply the inner function to each row's 'genres' column in the DataFrame to create a boolean mask for filtering.
    mask = df['genres'].apply(is_genre_match)
    # Use the boolean mask to filter the DataFrame, keeping only rows where the genre matches.
    filtered_movies = df[mask]
    return filtered_movies

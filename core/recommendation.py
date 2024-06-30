import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .models import Profile, Movie, Log, WatchList
from django.db.models.query import QuerySet

N_RECCOMENDATIONS = 6
FEATURES = [
    'War',
    'Comedy',
    'Documentary',
    'Crime',
    'Thriller',
    'Noir',
    'Science Fiction',
    'Action',
    'Adventure',
    'Animation',
    'Family',
    'Horror',
    'Western',
    'Romance',
    'Musical',
    'Mystery',
    'Drama',
    'Fantasy'
    ]

def get_liked_movies(profile: Profile) -> list[Movie]:
    return [log.movie for log in Log.objects.filter(profile=profile, like=True)]


def get_movie_vectors(movies: QuerySet[Movie]) -> dict[int, list[float]]:
    movie_vectors = {}
    
    for movie in movies:
        if movie.pk in movie_vectors:
            continue
        else:
            movie_vectors[movie.pk] = []
        for i in range(len(FEATURES)):
            movie_vectors[movie.pk].append(1 if FEATURES[i] in movie.genres else 0)
            
    return movie_vectors


def get_profile_average_vector(profile: Profile) -> list[float]:
    profile_average_vector = np.zeros(len(FEATURES))
    profile_movies = get_movie_vectors(get_liked_movies(profile))
    for movie_pk in profile_movies:
        profile_average_vector += np.array(profile_movies[movie_pk])
    return (profile_average_vector / len(profile_movies)) if len(profile_movies) > 0 else []


def calculate_similarity(profile: Profile, movies: dict[int, list[float]]) -> dict[int, float]:
    movie_pks = list(movies.keys())
    movie_vectors = np.array(list(movies.values()))
    
    profile_vector = get_profile_average_vector(profile)
    if profile_vector.size == 0:
        return None
    
    '''
    Reshapes the array into a 2-dimensional array with one row and as many columns 
    as needed to accommodate all the elements of the original array.
    So, if x is a 1-dimensional array with n elements, x.reshape(1, -1) 
    will convert it into a 2-dimensional array with 1 row and n columns.
    '''
    profile_vector_2D = profile_vector.reshape(1, -1)
    
    '''
    The result is a 2-dimensional array where each element is the similarity score between 
    the user_profile and a movie vector. By accessing the first element [0], 
    a 1-dimensional array of similarity scores is returned.
    '''
    similarities = cosine_similarity(profile_vector_2D, movie_vectors)[0]
    similarity_scores = {movie_pk: similarity for movie_pk, similarity in zip(movie_pks, similarities)}
    return similarity_scores


def get_recommended_movies(profile: Profile) -> list[int]:
    movie_vectors = get_movie_vectors(Movie.objects.all())
    watched_movies = [x.movie.pk for x in Log.objects.filter(profile=profile)]
    watchlisted_movies = [x.movie.pk for x in WatchList.objects.filter(profile=profile)]
    for movie_pk in (watchlisted_movies + watched_movies):
        if movie_pk in movie_vectors:
            del movie_vectors[movie_pk]
    
    if len(movie_vectors) == 0:
        return None
    
    similarity_scores = calculate_similarity(profile, movie_vectors)
    if not similarity_scores:
        return None
    
    sorted_movies = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    print(sorted_movies)
    return [Movie.objects.get(pk=x[0]) for x in sorted_movies[:N_RECCOMENDATIONS]]
# Cult
A webapp based on the paradigms that compose modern social networks and focussed on the cinematic art.

## Description
The website provides for the managment of a collection of movies and user profiles.  
Users can be anonymous or registered. Registered users are contained in one of the following categories:
"base", "business", "staff", "admin". Each category defines a set of permissions applied to the users in the group.

Services provided by the categories:
- **Anonymous user**
    - search and view movies
    - search and view profiles 
    - view movies reviews
    - register a profile
    - log into a profile
- **Registered user**
    - **Base profile**
        - operations provided by the previous categories
        - update the own profile (profile picture, biography)
        - follow (and unfollow) other profiles
        - log a movie (and delete a previously added log)
        - add a movie to the watchlist (and remove a movie from the watchlist)
        - add a logged movie to the favourites (and remove a movie from the favourites)
        - add a review of a logged movie (and delete a previously added review)
        - star a review (and remove a star)
        - log out
    - **Business profile**
        - operations provided by the previous categories
        - publish, update and delete a movie (CRUD operations)
    - **Staff**
        - operations provided by the Anonymous category
        - read and update operations on users
        - read and update operations on auth groups ("base", "business")
    - **Admin**
        - operations provided by the Anonymous category
        - maximum permissions
        - create, read, update, delete (CRUD) operations on User, Group, Review and Movie objects

Base profile represent the main user of the platform. While the business profile is designed for movies producers in order to publish their films.

Whenever a new user is registered, the system create a related profile. Each new profile is added to the "base" group, only a staff user or the admin may move a profile from the "base" group to the "business" one.  
Staff and admin users do not have a related profile, this is because they are users whose purpose is to ensure the proper functioning of the platform. They do not appear in profile searches and cannot be followed.

## Database
The following UML diagram shows the platform's database structure.

![cult_uml_diagram](/docs/cult_uml_diagram.png)

Observations:
- The database adopted is SQLite.
- Since Django framework does not support composite primary keys, each model has a non-composite primary key. In case location uniquness for multiple attributes is needed, a UniqueConstraint object is defined.
- Synchronization of database accesses is guaranteed by Django.

## Recommendation System
The recommendation system adopted is content-based. Although the system has been designed around the movie concept, it would be valid for any kind of discrete item.

Each movie is translated into a vector. Every element in the vector corresponds to a feature and its value (0,1) represents whether of not the item has that feature.  
In this case, the features are the set of genres:
```
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
```

The profile vector is defined as follows: every logged and liked movie of the profile is vectorized, the average resulting vector represents the profile cinematic taste.
$$\mathrm{\text{profile-vector}[i]} = \sum_{n=0}^{\text{number of liked movies}-1} \dfrac{\text{movie-vector n}[i]}{\text{number of liked movies}}$$
$$\text{where 0 <= i < len(FEATURES) is the i-th feature.}$$

Eventually, the system computes the cosine similarity between the profile vector and each movie vector that has not been logged or watchlisted by the profile. The result is ordered by similarity in descending order.
$$\mathrm{\text{cosine similarity of A and B}\to cos(\theta)} = \dfrac{AB}{\lVert A \rVert \lVert B \rVert}$$
$$\text{where } cos(\theta)=[0,1] \text{ because the vector elements cannot assume negative values.}$$

## Installation
To install the webapp, the latest release contains an already populated database for test purposes. It can be downloaded to test the features.

Otherwise, clone the repo:
```
git clone https://github.com/RaffaeleTranfaglia/Cult.git
```

Make sure `pipenv` is installed.  
Install dependencies:
```
pipenv install --anyway
```

Activate the virtual environment:
```
pipenv shell
```

Create migrations:
```
python manage.py makemigrations core
```

Migrate:
```
python manage.py migrate
```

Create the admin (superuser):
```
python manage.py createsuperuser
```

Start development server to run the webapp:
```
python manage.py runserver
```

Eventually, open on a browser the following url, `http://127.0.0.1:8000/` (local host IP address: 127.0.0.1, port: 8000).

## Testing
There are test-cases to verify the correct execution of certain segments of the software.  

The test-cases cover the following aspects:
- Check that when a user is registered, it is added to "base" group adn an associated profile is create. In case the user created is an admin or a staff user, this should not happen.
- Check that the view handling the logic for logging a movie executes correctly in every case, and that block users that does not have the right permissions or that are trying to log a movie that has not yet been released.

To run test-cases:
```
python manage.py test core
```

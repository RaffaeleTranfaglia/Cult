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
## Installation
## Testing

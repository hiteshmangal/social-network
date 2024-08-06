# Social Network API

This is a social networking API built with Django Rest Framework.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/hiteshmangal/social-network.git
    cd social_network
    ```


2. Build and start the Docker containers:

    ```sh
    docker-compose up --build
    ```

3. Apply migrations:

    ```sh
    docker-compose run web python manage.py migrate
    ```

4. Create a superuser:

    ```sh
    docker-compose run web python manage.py createsuperuser
    ```

5. The API will be available at http://localhost:8000/.

## API Endpoints

- `POST /users/signup/` - User signup
- `POST /users/login/` - User login
- `GET /users/search/?q=` - Search users by email or name
- `POST /friends/send-request/<user_id>/` - Send friend request
- `PATCH /friends/accept-request/<id>/` - Respond to friend request (accept/reject)
- `PUT /friends/reject-request/<id>/` - Respond to friend request (accept/reject)
- `GET /friends/friends/` - List friends
- `GET /friends/pending-requests/` - List pending friend requests



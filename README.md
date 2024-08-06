# Social Network API

This is a social networking API built with Django Rest Framework.

## Installation

1. Clone the repository:

    ```sh
    git clone <repository_url>
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

5. Access the API at `http://localhost:8000/`.

## API Endpoints

- `POST /api/signup/` - User signup
- `POST /api/login/` - User login
- `GET /api/search/?keyword=` - Search users by email or name
- `POST /api/friend-request/send/<user_id>/` - Send friend request
- `POST /api/friend-request/respond/<request_id>/<response>/` - Respond to friend request (accept/reject)
- `GET /api/friends/` - List friends
- `GET /api/friend-requests/pending/` - List pending friend requests
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
    curl --location 'http://127.0.0.1:8000/users/signup/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
            "email": "shubhi@gmail.com",
            "password": "shubhi",
            "first_name": "shubhi",
            "last_name": "shubhi"
            }'

            
- `POST /users/login/` - User login
    curl --location 'http://127.0.0.1:8000/users/login/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
    "email": "shubhi@gmail.com",
    "password": "shubhi"
    }'


- `GET /users/search/?q=` - Search users by email or name
    curl --location 'http://127.0.0.1:8000/users/search/?q=harshit' \
    --header 'Authorization: Bearer <your_access_token>'


- `POST /friends/send-request/<user_id>/` - Send friend request
    curl --location 'http://127.0.0.1:8000/friends/send-request/<user_id>/' \
    --header 'Authorization: Bearer <your_access_token>' \
    --header 'Content-Type: application/json' \
    --data '{
    "to_user": <user_id>
    }'

- `PATCH /friends/accept-request/<id>/` - Respond to friend request (accept/reject)
    curl --location --request PATCH 'http://127.0.0.1:8000/friends/accept-request/<id>/' \
    --header 'Authorization: Bearer <your_access_token>'


- `PUT /friends/reject-request/<id>/` - Respond to friend request (accept/reject)

    curl --location --request PUT 'http://127.0.0.1:8000/friends/reject-request/<id>/' \
    --header 'Authorization: Bearer <your_access_token>' \
    --header 'Content-Type: application/json' \
    --data '{
    "status": "rejected"
    }'
- `GET /friends/friends/` - List friends

    curl --location 'http://127.0.0.1:8000/friends/friends/' \
    --header 'Authorization: Bearer <your_access_token>'

- `GET /friends/pending-requests/` - List pending friend requests
    curl --location 'http://127.0.0.1:8000/friends/pending-requests/' \
    --header 'Authorization: Bearer <your_access_token>'



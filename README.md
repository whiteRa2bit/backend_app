<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li>
      <a href="#installation">Installation</a>
    </li>
    <li>
      <a href="#rest-api-description">REST API description</a>
    </li>
    <li>
      <a href="#license">License</a>
    </li>
    <li>
      <a href="#contact">Contact</a>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
Backend sample app using Docker Compose, MongoDB, Redis and Flask for managing resources.
Marshmallow is used for validating request and response schemas.

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.


### Installation

  1. Clone the repo
     ```sh
     git clone git@github.com:whiteRa2bit/backend_app.git
     ```
 
  2. Build
        ```
        docker-compose build .
        ```

  3. Compose up
        ```
        docker-compose up -d
        ```

## REST API description

### <a name="get-healtcheck"></a> 1: GET `/healtcheck`

### <a name="get-users"></a> 2: GET `/users`

### <a name="get-user"></a> 3: GET `/users/<string:user_id>`

### <a name="post-users"></a> 4: POST `/users`

### <a name="put-user"></a> 5: PUT `/users/<string:user_id>`

### <a name="delete-user"></a> 6: DELETE `/users/<string:user_id>`

### <a name="get-stats"></a> 7: GET `/stats/<string:user_id>`

### <a name="post-stats"></a> 8: POST `/stats/<string:user_id>`

### <a name="get-games"></a> 9: GET `/games`

### <a name="get-game"></a> 10: GET `/games/<string:game_id>`

### <a name="post-games"></a> 11: POST `/games`



## License

Distributed under the MIT License. See `LICENSE` for more information.


## Contact

Pavel Fakanov - pavel.fakanov@gmail.com

Project Link: [https://github.com/whiteRa2bit/mafia_grpc](https://github.com/whiteRa2bit/mafia_grpc)

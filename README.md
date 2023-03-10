# images_app
Web server that lets it's users to upload images and get links to their thumbnails.
Based on tier, user can get links to thumbnails of different heights or to original image.
Users can also have an ability to fetch expiring link to original image.

## Installation
To run dockerized verions of this project you need `docker-compose`.
Build and run containers with:
```
docker-compose up
```
If it's the first time you run these containers, run a shell in 'web' container:
```
docker exec -it images_app_web_1 /bin/bash
```
You may need to replace `images_app_web_1` with your container name.

Apply migrations:
```
python manage.py migrate
```
You can also create a super user:
```
python manage.py createsuperuser
```

## Endpoints
### `POST /api/images`
Lets you upload an image to server.
Only for authenticated users.

POST data:
```
{
    "image": <image_file>
}
```
### `GET /api/images`
Returns a list of your images with existing links to them.
Only for authenticated users.

### `GET /api/images/<image_url>`
Returns an image associated with this url

### `POST /api/expiring`
Lets you create expiring link to your image.
Only for authenticated users.

POST data:
```
{
    "image": <image_id>,
    "expiring": <seconds_to_expire>
}
```

## Testing
To run tests shell into web container and run:
```
python manage.py test
```

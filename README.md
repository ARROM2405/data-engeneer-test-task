# Test task for Data Engineering Internship

## Project structure.
Project is done with django REST framework as the HTTP requests and data processor, 
sqlite as the intermediate database, and minio as the permanent data storage.
App is being structured as 3 docker containers:
* Minio server.
* Django app.
* Utils.

## Operating process.

### Running the app.
1. The app is started with `docker-compose up`.
2. `minio` container starts minio server at `localhost:9001`.
3. `django-app` container starts django app at `localhost:8000`.
4. `my-utils` container runs a `create_bucket_and_upload_data.py` file that:
   1. creates bucket `source` at minio that has to be used to store data to be processed;
   2. uploads `.zip` file from `source_data` directory inside the project. That is the initial data upload to minio;
   3. sends POST request to django app `/data/` so the file uploaded in the previous step is 
   processed. POST requests are sent to the app each 55 minutes, so if there is new data uploaded, it 
   is automatically processed within an hour. 
5. All the data in order to be processed has to be uploaded to the `source` bucket in `.zip` format.

### HTTP requests.
Django app replies to the:
* `GET` request to `localhost:8000/data/` - returns processed data in `.json` format. Can be viewed in human-readable 
format with the browser as well.
* `POST` request to `localhost:8000/data/` - manually trigger reprocessing of the data file stored in the `source` 
bucket. Returns string 'updated'.
* `GET` request to `localhost:8000/stats/` - returns average value for births field of all objects in the queryset, 
length of the queryset and filters used in the string format. Filters can be added as the url arguments, example:
`http://localhost:8000/stats/?is_image_exists=False&min_age=1&max_age=2`. If no objects were returned by the filter,
a string 'Filter returned no objects' will be returned.

### Logging in to django admin and minio.
* Admin panel of the django app can be logged in at `localhost:8000/admin/`. Username - 'admin', password - 'admin'.
* Minio can be logged in at `localhost:9001`. Username - 'minioadmin', password - 'minioadmin'.

### Data processing logic.
1. App stores the datetime of the last data processing.
2. Django app connects to the minio and checks the file in the `source` bucket. If upload datetime of the file is later 
than the last processing, it will be downloaded for further steps. If not, following steps until step 9 are skipped.
3. `minio_data/minio_template.zip` is used to create via copying a new `.zip` file into which `.zip` from `source` 
bucket is downloaded.
4. All data is first stored to the `sqlite` db. That implementation is done so Django ORM can be used for convenient 
filtering of data and returning a `.json` format as the response for HTTP request.
5. Getting list of ids of all existing instances in  `sqlite` db, to check if they have to be updated with the data from
the new file, or have to be removed if not added to the new file. 
6. Iterating through each file in the `.zip` file, an instance of the `UserData` model is being created and saved to the
`sqlite` db. Removing ids from the list in previous step. 
7. All the instances with ids left in the list from step 5 are being removed, as they are not added to the new data 
file.
8. Iterating through all instances of the `UserData` and writing data to the `minio_data/output.csv`. Uploading the 
`minio_data/output.csv` to the `processed-data` bucket.
9. Updating processing datetime to the `LastUpdate` model.

### HTTP responses logic.
HTTP responses are being implemented with APIViews, models and serializers. Data for the HTTP response is being 
processed with django ORM.  
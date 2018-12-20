# WCA Data Django Application for SI 664 Fall 2018

## Purpose
Explore the data that is in the World Cube Association results database export

## Data set
This Django application uses the World Cube Associaion results database export, which can be found  [here](https://www.worldcubeassociation.org/results/misc/export.html). This application uses the export from 11/27/2018.

## Data model
<img src="./static/img/database model.png" alt="WCA database model">

## Package Dependencies
Taken from requirements.txt

* certifi
* chardet
* coreapi
* coreschema
* defusedxml
* Django
* django-allauth
* django-cors-headers
* django-crispy-forms
* django-filter
* django-rest-auth
* django-rest-swagger
* django-test-without-migrations
* djangorestframework
* idna
* itypes
* Jinja2
* Markdown
* MarkupSafe
* mysqlclient
* oauthlib
* openapi-codec
* pkg-resources
* PyJWT
* python3-openid
* pytz
* PyYAML
* requests
* requests-oauthlib
* simplejson
* six
* social-auth-app-django
* social-auth-core
* uritemplate
* urllib3

## Misc Notes:

* filters and forms can take a while to load and update (a few minutes to maybe half an hour)
* sql dump file is ~200MB so the sql dump is inside `.zip`
* the sql file that turns the WCA database export into a relational database can take ~30 hours to run
* my ID number in the application is 66687 with the WCA ID 2011CHEN54
* GET: [http://localhost:8000/wca/api/persons/{person id number}/](http://localhost:8000/wca/api/persons/{person id number}/)
* POST: [http://localhost:8000/wca/api/persons/](http://localhost:8000/wca/api/persons/)
```json
    {
        "person_identifier": "<WCA ID>",
        "person_name": "<person name>",
        "country_id": <country id number>,
        "gender": "<m. f, o, or none>",
        "result_ids": [<result id number>]
    }

```
* PUT: [http://localhost:8000/wca/api/persons/{person id number}/](http://localhost:8000/wca/api/persons/{person id number}/)
```json
    {
        "person_identifier": "<WCA ID>",
        "person_name": "<person name>",
        "country_id": <country id number>,
        "gender": "<m, f, o, or none>",
        "result_ids": [<result id number>]
    }
```



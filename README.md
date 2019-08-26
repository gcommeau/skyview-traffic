# Skyview Academy Student Pickup Web Application

# Context

Skyview Academy elementary students need to be picked up by their parents/caregivers via one of the 3 exit points:
- Carline: The parents stay in their cars and line up until volunteers bring the child(ren) to the car
- Walker: The parents wait outside the school in a dedicated area
- Preschool: Preschool students need to be signed out at this location

Skyview has a database of elementary students, each associated with a family number and a classroom. In order to pick up their children, the parents need to present their family number card to one of the volunteers.

The school used to have a system in place, but unfortunately, it recently partially stopped working. This web application provides a replacement for the previous system.


# Usage

This web application is mainly composed of 2 webpages:

1. One for the classroom view, for the teacher to display in class. The name of the students will appear in one of 3 columns: Walker, Carline and Preschool, corresponding to the location where the student is expected to meet the parent. Note that in order to save screen real-estate, the preschool column will only appear when necessary (most classrooms do not have students going through the preschool checkouts).

1. One for checking out students. The volunteers enter the family numbers as they flow in. Once a family number is entered and accepted, a confirmation message will appear, as well as a button to cancel in case the volunteer mistyped the number. As soon as the family number is entered, all the students' names of the family will appear in each respective classroom view.

The webapp also has an administrative console, which allows the admins to create/update/delete users and any kind of data entry present in the database (students, classrooms, etc).

The application requires user authentication in order to access the web pages, Rest API and admin console.


# Architecture

This is a [Django](https://www.djangoproject.com/) web application. The front-end templates use [Query](https://jquery.com/) to provide a dynamic user experience.

To provide scale and reliability, it is deployed using [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) with a [RDS](https://aws.amazon.com/rds/) (MySQL) database. The Beanstalk environment uses [an https listener](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/configuring-https.html) coupled with a public certificate to provide in-flight encryption.

# Development

1. Make sure python 3 is installed
```
python --version
```
1. Clone this git repository
1. (Optional but recommended) Setup a virtual environment
```
pip3 install virtualenv
virtualenv ~/skyview-traffic-dev
. ~/skyview-traffic-dev/bin/activate
```
1. Install project's dependencies
```
pip install -r requirements.txt
```
1. To run locally:
  1. Load local development settings
  ```
  mv settings.py.EXAMPLE settings.py
  ```
  1. Build a local database
  ```
  python manage.py migrate
  ```
  1. Load play data (Harry Potter theme)
  ```
  python manage.py loaddata traffic
  ```
  1. Start the Django server
  ```
  python manage.py runserver
  ```
  1. Navigate to the location pointed by Django (usually http://localhost:8000/)

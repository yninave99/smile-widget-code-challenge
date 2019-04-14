# smile-widget-code-challenge

The Smile Widget Company currently sells two types of smile widgets: a Big Widget and a Small Widget.  We'd like to add more flexibility to our product pricing.

## Setup with Docker
1. Install Docker (https://docs.docker.com/install/)
2. Clone this repository.
3. `>>> docker-compose up --build`

## Setup without Docker
1. Install Python (>3.4)
2. Install postgres.  By default the Django app will connect to the database named 'postgres'.  See `settings.DATABASES`.
3. Clone this repository.
4. Install requirements.
  * `>>> pip install -r requirements.txt`
5. Run migrations.
  * `>>> python manage.py migrate`
6. Load data from fixtures:
  * `>>> python manage.py loaddata 0001_fixtures.json`

### Technical Requirements
* We currently have to products with the following prices:
    * Big Widget - $1000
    * Small Widget - $99
* These products, along with existing gift cards are already setup in the database.  Study the existing models and initial data.
* Create a new ProductPrice model and setup the following price schedule:    
  * Black Friday Prices (November 23, 24, & 25)
    * Big Widget - $800
    * Small Widget - FREE!
  * 2019 Prices (starting January 1, 2019)
    * Big Widget - $1200
    * Small Widget - $125
* Build a JSON API endpoint that accepts a product code, date, and (optional) gift card and returns product price.
  * The endpoint should live at `api/get-price` and accept the following parameters:
    * `"productCode"`
    * `"date"`
    * `"giftCardCode"`
* Update this README file with instructions on how to run and access your price calculator.
* Create a pull request with your changes.

### Additional Information
* Please use Django Rest Framework or a Python web framework of your choice to create the endpoint.
* Just as a general guideline, we've designed this exercise to take less than 4 hours.

### Update
* Run 'pip install -r requirements.txt'
* Create a mysql database called as smilewidgets with the command 'create database smilewidgets;'
* Run 'python smilewidgets/manage.py makemigrations'
* Run 'bash startup-script.sh'
* Login to Database (Here Im using Mysql) and Run the below insert queries:
  * insert into products_productprice (amount, date_start, date_end, product_id_id) values (80000, "2018-11-23", "2018-11-25", 1);
  * insert into products_productprice (amount, date_start, date_end, product_id_id) values (00, "2018-11-23", "2018-11-25", 2);
  * insert into products_productprice (amount, date_start, product_id_id) values (120000, "2019-01-01", 1);
  * insert into products_productprice (amount, date_start, product_id_id) values (12500, "2019-01-01", 2); 
* Now you can go to '0.0.0.0:8000' and check the functionality

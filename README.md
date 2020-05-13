# MSiA 423 Dessert Flavor Evaluator 
Project creator and Developer: Safia Khouja   
(QA contributions: Daniel Halteh)   

- [Project Charter](#project-charter)
- [Project Backlog](#project-backlog)
## Project Charter 
### Vision 
Everybody loves dessert, but not everybody knows how to create delicious and exciting treats. This app helps dessert-lovers generate creative flavor combinations to explore in their own kitchens! Long-gone are the days of choosing between flavors like vanilla or chocolate. With the help of my app, dessert-lovers are inspired to bake and cook impressive new creations that combine classical flavors, refreshing fruits, and exciting spices 

### Mission 
Users will input a combination of dessert flavors and the app will predict the rating of this flavor combination. The app will also recommend the most popular desserts matching that flavor combination for inspiration. The data for this project was scraped from the popular recipe website Epicurious (https://www.kaggle.com/keytarrockstar/dessert-flavor-combinations/data, https://archive.org/download/recipes-en-201706/). 

Theoretical example: A user who is curious about the combination of vanilla + raspberry + rhubarb would enter those flavors into the app. The app would then predict that this flavor combination has a rating of 3.5/4 and suggest highly-rated desserts such as *Rhubarb and Raspberry Crostata* and *Rhubarb and Raspberry Jam Roly-Poly*. Based on this positive output, the user would then be empowered to pursue this flavor combination by baking one of the suggested desserts or creating a completely new recipe using these flavors.

### Success Criteria 
The model will be deployed if it can predict the ratings of flavor combinations in the test set with a cross validation R^2 of 0.7. To determine the business success of my app among users, standard A/B testing will be used to compare the average rating of desserts made by people who did not consult the app to the average rating of desserts made by people who consulted my app about the flavor profile they intended to pursue. Overall, a successful deployment of this app will help dessert-lovers create delicious and innovative desserts. 

## Project Backlog

Note: The description in italics after every story details the predicted size of story, backlog vs icebox status, and when the task is planned for. 

- **Initiative 1**: Build the model and recommender 
	- **Epic 1**: Develop model for potential production use that predicts the rating of a given flavor combination  
		- **Story 1**: Learn more about the data to better understand how Epicurious and its readers collect, interact with, and use the data. *(small, backlog, next two weeks)*
		- **Story 2**: Scrape data from Epicurious to add a column for number of reviews to the dataset. The number of reviews will help contextualize the rating. *(medium, backlog, next two weeks)*
		- **Story 3**: Perform exploratory data analysis *(small, backlog, next two weeks)*
		- **Story 4**: Clean data by taking care of missing values, repeated values, and confusing values. Make the flavor values into dummy variables and drop irrelevant flavors. *(medium, backlog, next two weeks)*
		- **Story 5**: Split the data into a training and testing set *(x-small, backlog)*
		- **Story 6**: Test several supervised learning methods on the data, including random forest, XGBoost, and neural networks. Use cross validation to determine which model fits the data best. *(x-large, backlog)*
		- **Story 7**: Try out additional models *(icebox)*
		- **Story 8**: Select best model. Review model and accompanying code with QA partner *(medium, backlog)*

	- **Epic 2**: Develop a dessert recommender for potential production use that suggests popular recipes based on the inputted flavor combination 
		- **Story 1**: Write code to filter recipes by flavor combination. *(small, backlog, next two weeks)* 
		- **Story 2**: Write code to determine the most popular recipes post-filtering, taking into account both rating and number of ratings *(medium, backlog, next two weeks)* 
		- **Story 3**: Determine the best way to present recipe suggestions along with their ratings *(small, backlog, next two weeks)* 
		- **Story 4**: Review recipe suggestion process and accompanying code with QA partner *(medium, backlog)*

- **Initiative 2**: Application Development and Cloud Infrastructure
	- **Epic 1**: Backend development and cloud setup to support the application
		- **Story 1**: Set up environment and Docker. *(medium, backlog, next two weeks)* 
		- **Story 2**: Employ a running RDS instance. *(medium, backlog)*
		- **Story 3**: Use an S3 bucket to store the data.  *(medium, backlog)*
		- **Story 4**: Migrate code to scripts and incorporate model and recommender into the app *(medium, backlog)*
		- **Story 5**: Write unit tests and log *(to be done throughout the process)* 
		- **Story 6**: Review and test the requirements file *(small, backlog)*

	- **Epic 2**: Frontend development to create a user-friendly interface 
		- **Story 1**: Create application using HTML/CSS and Flask *(large, backlog)* 
		- **Story 2**: Put finishing touches and improve GUI *(medium, backlog)* 

- **Initiative 3**: Final product and evaluation
	- **Epic 1**: Create the final product
		- **Story 1**: Finalize Github repository *(medium, backlog)* 
		- **Story 2**: Create final presentation *(long, backlog)* 
	- **Epic 2**: Evaluate product success from a business standpoint
		- **Story 1**: Evaluate product success using A/B testing *(icebox)* 
		- **Story 2**: Evaluate user engagement by tracking clicks *(icebox)*


## Midpoint Pull Request 
### Downloading the data and Uploading it to an S3 Bucket 
2. Retrieve desserts.csv from Kaggle
    - My primary dessert data comes from a static data file located behind the Kaggle paywall. As a result, the file
     can only be downloaded manually from https://www.kaggle.com/keytarrockstar/dessert-flavor-combinations. The file, 
     originally named recipes.csv, was renamed desserts.csv to avoid mixing up the two datasets used for this project. 
     Next, desserts.csv, was saved in the data/external folder. For other users, the location of the data is configurable in congif.py 
     as the DESSERTS_PATH variable

3. Download epicurious_recipes.csv using 
    - I use secondary data from a static, public, data file to supplement my primary data. This file, which contains a recipe
     of over 30K Epicurious recipes (not just dessert recipes) is large (84 MB)
   
    (This file provides additional 
    contextualizing information, like how many users rated each item ) 





## Project Template
<!-- toc -->

- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Initialize the database](#1-initialize-the-database)
    + [Create the database with a single song](#create-the-database-with-a-single-song)
    + [Adding additional songs](#adding-additional-songs)
    + [Defining your engine string](#defining-your-engine-string)
      - [Local SQLite database](#local-sqlite-database)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Run the Flask app](#3-run-the-flask-app)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
  * [3. Kill the container](#3-kill-the-container)
  * [Workaround for potential Docker problem for Windows.](#workaround-for-potential-docker-problem-for-windows)

<!-- tocstop -->

## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Running the app
### 1. Initialize the database 

#### Create the database with a single song 
To create the database in the location configured in `config.py` with one initial song, run: 

`python run.py create_db --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py create_db` creates a database at `sqlite:///data/tracks.db` with the initial song *Radar* by Britney spears. 
#### Adding additional songs 
To add an additional song:

`python run.py ingest --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py ingest` adds *Minor Cause* by Emancipator to the SQLite database located in `sqlite:///data/tracks.db`.

#### Defining your engine string 
A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). We will cover SQLAlchemy and connection strings in the SQLAlchemy lab session on 
##### Local SQLite database 

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/tracks.db'

```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory).

You can also define the absolute path with four `////`, for example:

```python
engine_string = 'sqlite://///Users/cmawer/Repos/2020-MSIA423-template-repository/data/tracks.db'
```


### 2. Configure Flask app 

`config/flaskconfig.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
HOST = "0.0.0.0" # the host that is running the app. 0.0.0.0 when running locally 
PORT = 5000  # What port to expose app on. Must be the same as the port exposed in app/Dockerfile 
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/tracks.db'  # URI (engine string) for database that contains tracks
APP_NAME = "penny-lane"
SQLALCHEMY_TRACK_MODIFICATIONS = True 
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100 # Limits the number of rows returned from the database 
```

### 3. Run the Flask app 

To run the Flask app, run: 

```bash
python app.py
```

You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

## Running the app in Docker 

### 1. Build the image 

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo): 

```bash
 docker build -f app/Dockerfile -t pennylane .
```

This command builds the Docker image, with the tag `pennylane`, based on the instructions in `app/Dockerfile` and the files existing in this directory.
 
### 2. Run the container 

To run the app, run from this directory: 

```bash
docker run -p 5000:5000 --name test pennylane
```
You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

This command runs the `pennylane` image as a container named `test` and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port. 

If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `app/Dockerfile`)

### 3. Kill the container 

Once finished with the app, you will need to kill the container. To do so: 

```bash
docker kill test 
```

where `test` is the name given in the `docker run` command.

### Workaround for potential Docker problem for Windows.

It is possible that Docker will have a problem with the bash script `app/boot.sh` that is used when running on a Windows machine. Windows can encode the script wrongly so that when it copies over to the Docker image, it is corrupted. If this happens to you, try using the alternate Dockerfile, `app/Dockerfile_windows`, i.e.:

```bash
 docker build -f app/Dockerfile_windows -t pennylane .
```

then run the same `docker run` command: 

```bash
docker run -p 5000:5000 --name test pennylane
```

The new image defines the entry command as `python3 app.py` instead of `./boot.sh`. Building the sample PennyLane image this way will require initializing the database prior to building the image so that it is copied over, rather than created when the container is run. Therefore, please **do the step [Create the database with a single song](#create-the-database-with-a-single-song) above before building the image**.

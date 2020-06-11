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



## Final Deliverable  
1. Build the model pipeline 
    - (Optional) Alter some or all of the default configurations in the .yaml in the config folder to suit your needs. Configurations such as the S3 database name, 
    SQLite directory, and file locations can be changed. Make sure that you never include spaces between the variable name 
    and the variable value in the .yaml file. 
    - Set your AWS credentials as environment variables to enable S3 access. Enter the following lines into your command 
    line after replacing the <AWS_access_key_id> and <AWS_secret_access_key} with your own credentials. 
        ```bash
        export AWS_ACCESS_KEY_ID=<AWS_access_key_id> 
        export AWS_SECRET_ACCESS_KEY=<AWS_secret_access_key}
        ```
        For reference, a SQL Alchemy URI for AWS RDS should be in the format below: 
            `dialect+driver://username:password@host:port/database`
    - Run the pipeline by entering the following lines into your command line. These commands build the Docker image and 
    then run the Docker container. The second command will source the AWS environment variables that you set above and 
    expose them in the Docker image. 
        ```bash
        docker build -t pipeline .
        docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(pwd)"/data,target=/app/data pipeline driver.py
        ```
   
2. Deploy the app 
    - (Optional) Set your SQLite URI for the SQL Alchemy engine string as an environment variable. Replace <SQL_alchemy_database_URI>
    with whatever database URI you want to use and run the following line in your command line. 
    `   ``{bash}
        export SQLALCHEMY_DATABASE_URI=<SQL_alchemy_database_URI> 
        ```
        - If you do not set the SQL_ALCHEMY_DATABASE_URI, the app will automatically build a SQLite database at the 
      location specified in the configuration file. You can change the directory location of the SQLite database in the SQLite section of the .yaml file
        - If you would prefer to set the configurations for your AWS RDS database within the code, fill in the 
      configurations in the AWSRDSDatabase section of the file. Make sure to set the buildAWSRDS flag in the same section to True to build to AWS RDS instead of local SQLite.
    - Run the app by entering the following lines into your command line. Each time that you run this command after the first deployment, you will have to 
      change the name of the container. The name of the container is the second to last word, the word to the left 
      of dessertflavorevaluator. In the command provided below the container is named "app", but this name can be changed to any 
      word (without spaces) after your initial deployment.  
        ```{bash}
        docker build -f app/Dockerfile -t dessertflavorevaluator .
        docker run -e SQLALCHEMY_DATABASE_URI -p 5000:5000 --name app dessertflavorevaluator
        ```
    - Kill the app when you are done using it. If it is not the first deployment, replace app with whatever you named 
    the container in the line above. 
        ```{bash}
        docker kill app
        ```
      
3. (Optional) Test the app 
    - Run the lines below in your command line to run the unit tests 
        ```{bash}
        docker build -t pipeline .
        docker run pipeline -m pytest
        ```

## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── templates/                    <- HTML code
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│
├── data                              <- Folder that contains data used or generated
│   ├── database/                     <- Location of the local SQLite database
│   ├── external/                     <- Data downloaded from the internet (either through code or manually)
│   ├── model/                        <- Trained model object, model artifacts, and trained model metrics
│
├── deliverables/                     <- Presentation
│
├── src/                              <- Source code for the project 
│
├── test/                             <- Files necessary for running model tests 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of of some of the src scripts for app deployment
├── driver.py                         <- Simplifies the execution of the src scripts for the model pipeline 
├── requirements.txt                  <- Python package dependencies 
```

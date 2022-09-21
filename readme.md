# Machine learning Project for Supply Chain

## Chain of events


### Setting up things
    1. Created a virtual environment
    '''
    python -m venev penv
    OR
    conda create -p penv
    '''

    2. Install the requirements.txt file
    '''
    pip install -r reuirements.tx
    '''

    3. We create a basic Hello World Flask app

    4. Pushed the updated repo to Git

    5. Setting up CI/CD Pipeline in our heroku app
    We will retrieve Heroku account's registered email id, Heroku API key, and application name

        a. Create a Dockerfile
        Enter commands that will run on the virtual machine on the hosting platform

        b. Create .dockerignore file, that will not include those files mentioned inside this file when image is built in the container.

        c. Just for testing, run 
        -------
        Build Docker Image command

        docker build -t <image-name>:<tagname>
        NOTE - Image name for docker must be in lowercase
        -------
        List Docker images in local system

        docker images
        -------
        Run docker image

        docker run -p <Port#>:<Port#> -e PORT=<Port#> ImageID

        like,
        docker run -p 5000:5000-e PORT=5000 f8c749e73678
        -------
        To check running container in docker

        docker ps
        -------
        To stop Docker container

        docker stop <container_id>
        -------
    
        d. Pushing changes to github.

        e. Create a .github/workflows directory and add main.yaml file containing the continous deployement instructions.

        f. Push changes to github.

    6. Creating a setup.py file, to install requiremtns and other packages automatically. And, to run the setup file use,

    python setup.py install

    7. Created basic structure for "premium" package. Meaning, we creat "logger", "exception", "component", "config", "pipeline" and "entity" packages inside "premium" package.

###  Let's code

    1. Starting with "logger" module, we write loggin configuration into its __init__.py file.

    2. Now we design our "exception" module

    3. Now under our Enity directory, we'll create config_entity.py in which we design the structure of what details we would require for our configuration to work, which pipeline file will use.


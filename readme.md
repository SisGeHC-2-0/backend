This repository is intended to store my Sotware Analysis and Projec discipline. The changes over this project should also follow the principles of [gitflow priciples](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) ([pt-br reference](https://www.alura.com.br/artigos/git-flow-o-que-e-como-quando-utilizar?srsltid=AfmBOopWBO8J2FISCs6m2N_ZMv6-x_oAnNZbJDzfPoWzUoW4gXzzhAvD))

# Setup

To run the application it is required to have installed [python](https://www.python.org/). Having [docker](https://www.docker.com/) is optional but it makes the PostgreSQL installation easier.

In the project root folder you can run 

```
    docker compose up  # you may need to run sudo at the beggining.
```

After running this command you should have a postgres instance running locally.

If you already have postgres installed or really dont want to use docker you should also donwload [PostgreSQL](https://www.postgresql.org/download/).

After the installation configure the db configurations at proj/settings.py, adjusting your values at this constant

```
    ...

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres', 
            'USER': 'postgres',
            'PASSWORD': 'example',
            'HOST': '127.0.0.1', 
            'PORT': '5432',
        }
    }

    ...
```

At this point, if you havent already installed the requirements.txt in a virtual environment, do it with the command

```
    pip install -r requirements.txt
```

With the db running it is necessary to also apply the migrations with the command

```
    python manage.py migrate # Yes "manage.py" is the file at the root folder.

    
    # I havent really tested this because i've built the project
    # direcly in my machine and dont really know how it will
    # work in a diferent machine.

    # So if you tested this and worked or you have found a solution
    # please fell free to correct this segment.
```

If you also want to populate the db with some dummy data, you can just run the populate_db.py script


```
    python populate_db.py
```

Eventually a setup script is going to be made.

# Running the application

To run the project you should just execute the following

```
    python manage.py runserver
```
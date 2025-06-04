# a demonstration for good security habits in web developmen
A web system for an imaginary communications company called Comunication_LTD. This company markets Internet browsing packages and its database contains information about the company's customers, the various browsing packages, and the sectors to which it markets its products. 
## the company seem to be really into shrek
so lots of shrek themed easter eggs can be found all over the project
we hope you enjoy browsing around the company site

## having trouble?
make sure you have a `.env` file with the correct variable names

This is our Example :)
```angular2html
MYSQL_ROOT_PASSWORD=toor
DB_HOST=localhost
DB_USER=shrek
DB_PASS=IHateDonkey
DB_DBNAME=shrekisloveDB
HMAC_SECRET_KEY = ShrekTheBest9000XXXKILLERXXX1234
```


## Docker Initialization
Make sure you are running the project with docker.
```dockerfile
docker compose build
docker compose up
```

## MySQL user init
make sure the user configured in env is also being build in your MySQL Server
```mysql
CREATE USER IF NOT EXISTS 'shrek'@'%' IDENTIFIED BY 'IHateDonkey';
GRANT ALL PRIVILEGES ON *.* TO 'shrek'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

like that ^^

#### make sure that file wait-for-mysql.sh is set for LF file system unicode so that docker will be able to execute it.

## for the Forgot Password functionalities:
you will need to sign up to the "mailtrap" service:
https://mailtrap.io/

then copy the username & password credentials from your virtual inbox to your local website server in the project (under the forgot password path in [app.py] )

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

make sure that file wait-for-mysql.sh is set for LF file system unicode so that docker will be able to execute it.
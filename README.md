# PSGC API

Based on https://psgc.gitlab.io/api/, but tweaked to suite my project's needs and updated to use the latest data from the [Philippine Statistics Authority](https://psa.gov.ph/). Try it out here: https://psgc-fastapi.onrender.com/docs.

See [Installation](#installation) section for instructions on how to install and setup this project for local development.

## Notes on Philippine Standard Geographic Code Revision 1

**TL;DR:** *The coding scheme was updated from 9 digits to 10 digits. The 4 NCR districts do not have a 10 digit code, and thus are not included in this API. Cities with high densities are now classified as Highly Urbanized Cities (HUCs) and have their own province code. This it's no longer possible to find which provinces they belong to based on their province code and they no longer show up under their corresponding provinces.*

As per Philippine Standard Geographic Code Revision 1, the coding scheme was updated from 9 digits to 10 digits. The province code section of the code was changed from 2 digits to 3 digits.

![New Coding Structure](./images/coding%20structure%20revision.png)

Apart from the coding changes, there were also 2 major changes.

**1) First, the 4 NCR districts were excluded from the adoption of the new coding scheme.** In the old scheme, the 4 NCR districts were assigned a province code so they were essentially the same level as a province. However in the new scheme, they were excluded and no longer have a code. Thus they are not included in this API.

![](./images/NCR%20districts.png)

As you can see, even on the [PSA website](https://psa.gov.ph/classification/psgc/regions), the 4 NCR districts don't have their own page unlike the provinces (as you can see on CAR for example).

**2) Second, cities with high densities are now classified as Highly Urbanized Cities (HUCs).** HUCs are given their own province code. The implication of this is that it's no longer possible to find which province the HUCs belongs to based on their province code. Even on the [PSA website](https://psa.gov.ph/classification/psgc/regions), the HUCs are no longer listed under their corresponding provinces.

![](./images/region%20XI%20cities.png)

For example, in the above screenshot taken from the [PSA website](https://psa.gov.ph/classification/psgc/citimuni/1102400000), it shows that the City of Digos is the only city in Davao del Sur. However, if you look geographically, there should be more cities in Davao del Sur, most notably Davao City. This is because in the latest scheme, Davao City is now classified as an HUC. As an HUC, it has its own province code, and thus no longer shows up under Davao del Sur. This applies to all cities now classified as HUCs.

If using this in address forms, it's advised to get the list of cities from the Region level instead, and just filter the cities based on user input.

For more information on the changes, see the [National Dissemination Forum on the 2019 Updates to the 2009 PSIC and Philippine Standard Geographic Code Revision 1](https://www.facebook.com/PSAgovph/videos/national-dissemination-forum-on-the-2019-updates-to-the-2009-psic-and-philippine/1738660179820236/) (PSGC Revision 1 is covered at around 1:45:00).


## Installation

This project is composed of 2 parts: the database and the API. The database is a [PostgreSQL](https://www.postgresql.org/) database and the API is built using [FastAPI](https://fastapi.tiangolo.com/).

### Database

1. Install PostgreSQL. You can download it [here](https://www.postgresql.org/download/). Alternatively, you can use a service like [Google Cloud SQL](https://cloud.google.com/sql) or [Amazon RDS](https://aws.amazon.com/rds/). Check the documentation of your chosen service for instructions on how to setup a PostgreSQL database.
2. Once the database is setup, set the `SQLALCHEMY_DATABASE_URI` environment variable to the connection string of your database. For example, if you're using a local PostgreSQL database, you can set it to `postgresql://<db user>:<db password>@localhost:5432/<db name>`.
```bash
export SQLALCHEMY_DATABASE_URI=postgresql://<db user>:<db password>@localhost:5432/<db name>
```
3. If you haven't installed the dependencies yet, install them by running:
```bash
pip install -r requirements.txt
```
4. Run alembic to setup the database and create the necessary tables.
```bash
alembic upgrade head
```
5. Run the setup script (WIP) to scrape the data from the [PSA website](https://psa.gov.ph/classification/psgc/) and populate the database. This will take a while.
```bash
python script/main.py
```

Once the setup script is done, the database is now ready to be used by the API.

### API

1. If you haven't installed the dependencies yet, install them by running:
```bash
pip install -r requirements.txt
```
2. Set the `SQLALCHEMY_DATABASE_URI` environment variable to the connection string of your database. For example, if you're using a local PostgreSQL database, you can set it to `postgresql://<db user>:<db password>@localhost:5432/<db name>`.
```bash
export SQLALCHEMY_DATABASE_URI=postgresql://<db user>:<db password>@localhost:5432/<db name>
```
3. Run the API using uvicorn.
```bash
python app/main.py
# or for production
uvicorn main:app --host 0.0.0.0 --port 80
```

If everything went well, you should be able to access the API documentation at http://localhost:8000/docs.

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
# Wieramemo_vase
## A simple python web crawler

### Description
Wieramemo_vase is a simple mutli-threaded python web crawler, made using the Selenium library and Python 3.9. To store data it uses PostgreSQL database.

### Instructions
The database can be found at: https://siasky.net/CAD4guRD0D3cD9pU6Hl1qlQNiaZOWFWdAGKAQZwPILhU_Q
To run the crawler, we move into the /crawler directory and run:

`py main.py`

Basic parameters like number of threads and the starting seed of sites can be configured in **main.py**, while the database settings can be modified in the **db_methods.py** file.
More specific parameters can be adjusted in the **crawler.py** file.

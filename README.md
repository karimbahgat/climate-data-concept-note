# DHIS2 Climate Data Connectors - Concept Note

New decentralized approach for importing and visualizing climate data in DHIS2, CHAP, and other apps. 


## What is it? 

- A set of templates and instructions for how countries can create their own climate data connectors.
- A climate data connector is:
    - Github repo w dockerfile and instructions for how to setup
    - The dockerfile should run a service that follows the api that Abyout is defining
    - Each local implementation of a data connector should require its own auth credentials if needed and instructions for how to get them


## Example (pending final api)

- When a climate data connector is run with docker compose up, it should expose (pending final api):
    - Required endpoint "list": lists all available datasets including metadata defining the aggregation function and maybe also map styling.
    - Main endpoint "aggregate": taking requests for a dataset, geometry, and time period, and returning aggregated data. 
    - Optional endpoint "data" but not required: could return raw gridded data for a region (e.g. needed in chap core). This could serve gridded data directly from a raster data source, or be generated dynamically on demand, e.g. by simulating up-to-date grid forecasts from live station data using [pycpt](https://iri-pycpt.github.io/). 
    - Optional endpoint "tileserver" but not required: dynamically returns xyz raster tiles for a given map extent and zoom to be used for visualizing the data in web maps. If the tileserver already exists, then the tiles are downloaded by the data connector and passed on to the user. 


## Benefits

- **Deduplication**: These climate data connectors can serve multiple needs in one solution and avoids duplicate efforts:
    - a standardized way to explore and import new self-contained data sources to climate app (e.g. forecasts from copernicus)
    - a standardized way for countries to support local data sources
    - can be used by chap to add support for gridded data
    - can be used by any other app that needs climate data, e.g. flood app
    - over time replace the hardcoded frontend solution for google earth with a more modular approach

- **Sharing**: Once a country creates such a data connector repo, this can be shared and used by anyone else. 

- **Flexibiliy**: It’s entirely up to each country how to connect to different data sources, can use any programming language or software stack.

- **Engagement**: It also encourages and lines up with existing efforts by different countries to connect to their own local data sources. 

- **Familiarity**: It mimics the mode of contribution used for chap models. 

- **Resources/Maintenance**: With this decentralized approach and local hosting by each country, it avoids a massive server and support burden on the climate team. 


## So where does the climate/chap team fit in? 

### Defining the standard api

- `dhis2/climate-data-api`
    - Contains text documents and GitHub Pages detailing the required API for climate data connectors

### Providing a minimalist example repo with dockerfile and instructions to setup a local server for each country. 

- `dhis2/climate-data-example-python`
    - Dockerfile w requirements for requests, fastapi
    - Docker compose that runs fastapi server
    - A fastapi route with an empty aggregate endpoint, to be filled by user

### Developing some data connectors to give countries a good start, eg to copernicus/era5 or google earth

- `dhis2/climate-data-local-test`
    - Python example or tutorial for a climate data connector showing how to symlink a local data folder during docker compose, and uses those files as local datasets to expose through the api
- `dhis2/climate-data-copernicus-forecast`
    - Instructions to create account and get credentials file
    - Instructions to manually approve license terms for forecast
    - Define list of Copernicus forecast datasets to expose
    - Using Copernicus `cdsapi` to fetch forecast grids and compute regional stats inside "aggregate" endpoint

### Updating the climate app to be able to connect to one or more such data stores

- In settings, user can add one or more urls to climate data connectors
- Climate app then allows choosing between datasets across different data connectors, facilitating easier comparisons across data sources

### Provide a python toolkit with utility functions to make data fetching and calculating aggregations easier for python based data connectors

- `dhis2/climate-data-utils-python`
    - Contains convenience funcs to calculate raster stats or serve gridded data

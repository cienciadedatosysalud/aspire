![Logo of the project](https://cienciadedatosysalud.org/wp-content/uploads/logo-Data-Science-VPM.png)

- [ASPIRE (Analytic Software Pipeline Interface for Reproducible Execution)](#aspire-analytic-software-pipeline-interface-for-reproducible-execution)
  - [ASPIRE Structure](#aspire-structure)
  - [Requirements/Dependencies](#requirementsdependencies)
  - [How to deploy it](#how-to-deploy-it)
  - [How to use the application](#how-to-use-the-application)
- [Authoring](#authoring)
- [How to contribute](#how-to-contribute)
- [Links of interest to manage R and Python dependencies for the analyses](#links-of-interest-to-manage-r-and-python-dependencies-for-the-analyses)
- [References](#references)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

# ASPIRE (Analytic Software Pipeline Interface for Reproducible Execution)

ASPIRE is a tool that allows you to containerize real life data analysis pipelines developed in Python or R in a simple, standardized and transparent way to enable reproducibility and ease of deployment in a federated approach. These projects follow the structure build using the [Common Data Model Builder](https://github.com/cienciadedatosysalud/cdmb), a tool that allows you to create common data models to facilitate interoperability and reproducibility of the analyses.


## ASPIRE Structure
The repository contains the following folders:

•  **gui_aspire**: Graphical interface developed in [Svelte](https://svelte.dev/), a JavaScript framework that allows you to create interactive and dynamic web applications.

•  **api_aspire**: The API developed with [FastAPI](https://fastapi.tiangolo.com/), a Python framework that allows you to create high-performance and easy-to-document RESTful APIs. The API handles the user interactions with the graphical interface and the deployed projects.

•  **projects**:  Folder where the projects you want to deploy in the application are stored. Each project must have its own subfolder with the project name and contain the files and folders necessary for its execution.


## Requirements/Dependencies

To run the Docker container, you need to have [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed on your machine. In addition, you must ensure that the container has installed the minimum dependencies for its operation. These dependencies are specified in the **_env.yaml_** file of the repository.

You should also keep in mind that each project may have its own dependencies, such as libraries or packages specific to data analysis. These dependencies should be indicated in the **_env.yaml_** file or, failing that, in the Dockerfile. Any incompatibility issues between packages and versions will stop building the image.

## How to deploy it

To deploy the Docker container, you must follow these steps:

1. Clone or download the repository from <a href="https://github.com/cienciadedatosysalud/ASPIRE">GitHub</a> to your local machine.
2. Open a terminal and navigate to the repository folder.
3. Copy the project's folder structure obtained from <a href="https://github.com/cienciadedatosysalud/cdmb">Common Data Model Builder</a> into the **projects** folder.
4. Modify the **_env.yaml_** file, adding the dependencies that your project needs to run correctly.
5. Run the command `docker-compose up` in the Terminal to build and run the container.Wait for the container to be ready after installing all the dependencies correctly.
6. Open a web browser and access the address http://<APP_HOST>:<APP_PORT> to see the graphical user interface of the application (by default <a href="http://localhost:3000">http://localhost:3000</a>).

## How to use the application
The application allows you to view and execute the data analysis projects that you have previously imported. To use the application, you must follow these steps:

1. On the main screen, you will see an animation of the steps to follow to execute a project.
2. __MAP DATA__: Select the project you want to map data to and select csv files. When everything is ready, click on `MAP AND CHECK YOUR DATA` button and wait for process to finish. Check output logs to verify that everything has been executed correctly.
3. __RUN ANALYSIS__: Select project from which you want to run analysis. Next select, from list of scripts found, main script of your analysis, in case of having dependent files among them. Finish by clicking on `RUN ANALYSIS` button and check that everything has been executed correctly.
4. __OUTPUTS__: In this section you will be able to see  and download, for all projects loaded in application, different output files for every process executed within ASPIRE tool, such as logs, html reports, csv aggregated outputs, etc.


# Authoring
ASPIRE has been developed by the [Data Science for Health Services and Policy research group](https://cienciadedatosysalud.org/en/us/research-group/)
in the Institute for Health Sciences in Aragón (IACS).

Lead by ![orcid](https://orcid.org/sites/default/files/images/orcid_16x16.png) [Javier González-Galindo](https://orcid.org/0000-0002-8783-5478)
, with the colaboration of ![orcid](https://orcid.org/sites/default/files/images/orcid_16x16.png) [Francisco Estupiñán-Romero](https://orcid.org/0000-0002-6285-8120), 
and ![orcid](https://orcid.org/sites/default/files/images/orcid_16x16.png) [Santiago Royo-Sierra](https://orcid.org/0000-0002-0048-4370)
, under the supervision and coordination of ![orcid](https://orcid.org/sites/default/files/images/orcid_16x16.png) [Enrique Bernal-Delgado](https://orcid.org/0000-0002-0961-3298) **(PI)**.

# How to contribute
- Repository: https://github.com/cienciadedatosysalud/ASPIRE/
- Issue tracker: https://github.com/cienciadedatosysalud/ASPIRE/issues

## Translate ASPIRE to your language

ASPIRE uses [i18n for Svelte](https://github.com/kaisermann/svelte-i18n) for internationalization.

Currently ASPIRE supports English by default and Spanish. Language selection is based on the default language set in your browser.

You can contribute adding another language by downloading the [en.json](https://github.com/cienciadedatosysalud/aspire/blob/main/gui_aspire/src/lib/i18n/locales/en.json) file, modify the json file without changing the value of the keys and changing each value to your language. It is important to respect all punctuation marks and escape characters.

Save the translated .json file as <your_language_code>.json.  "your_language_code" must follow the [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) standard.

Make a pull request to add your language. 

# Links of interest to manage R and Python dependencies for the analyses
- Micromamba: https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html
- Manage Dependencies with the deps R Package: https://hosting.analythium.io/manage-dependencies-with-the-deps-r-package-for-docker-containers/
- Package 'deps': https://cran.r-project.org/web/packages/deps/deps.pdf

# References
- Common Data Model Builder: https://github.com/cienciadedatosysalud/cdmb

[![DOI](https://zenodo.org/badge/663471048.svg)](https://zenodo.org/badge/latestdoi/663471048)
<a href="hhttps://creativecommons.org/licenses/by-nc/4.0/" target="_blank" ><img src="https://img.shields.io/badge/license-CC--BY--NC%204.0-lightgrey" alt="License: CC-BY-NC 4.0"></a>

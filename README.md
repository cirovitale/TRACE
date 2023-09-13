# TRACE: Tool for community Repositories Analysis and Cultural dispersion Examination
<p align="center"><img src="https://github.com/cirovitale/TRACE/blob/main/client/public/logo.png"></img></p>

- [ENGLISH VERSION](#english-version)
- [ITALIAN VERSION](#italian-version)
___
# ENGLISH VERSION
## Index
- [Introduction](#introduction)
- [Repository Structure](#repository-structure)
- [System Requirements](#system-requirements)
- [Installation](#installation)
  - [Server Configuration](#server-configuration)
  - [Client Configuration](#client-configuration)
- [Usage](#usage)
  - [Server Startup](#server-startup)
  - [Client Startup](#client-startup)
  - [Tool User Guide](#tool-user-guide)


## Introduction

The ***TRACE*** tool, developed as part of my Bachelor's thesis in Computer Science at the University of Salerno, is designed to analyse GitHub repositories, with the main purpose of calculating the Cultural Dispersion in a community of developers. The main challenge lies in identifying a developer's Culture from the limited information provided by a GitHub account. This identification is crucial, since it is subsequently used in the calculation of Cultural Dispersion, through the application of Shannon's Index.
The tool has been designed with a *client-server* structure, exploiting the potential of two modern technologies: `React` for the front-end and `Flask` for the back-end. Flask processes requests by exploiting **mathematical formulas**, **artificial intelligence techniques**, **predictive models** and **API calls** to an online service to ensure the processing of an accurate result.
For more details, we recommend reading the <a href="https://github.com/cirovitale/TRACE/blob/main/thesis/CiroVitale_BachelorThesis_2023.pdf" target="_blank">Thesis</a>, in Italian.

## Repository Structure
- `client` directory: client based on React.
- `server` directory: server based on Flask.
- `thesis` directory: Thesis.

## System Requirements
- **Memory**: minimum of 16 GB RAM to support in-memory loading of ML model.
- **Internet connection**: required for API calls. 

## Installation

Clone the repository.

### Server Configuration

1. **Download and Configure Assets**
    - Download the <a href="tinyurl.com/TRACE-ML-ASSETS" target="_blank">TRACE_ML_ASSETS</a> archive containing the directories, `models` and `vectorizers`.
    - Transfer `models` and `vectorizers` directories to the `server` directory.

2. **Create `.env` file**
    - Create a file called `.env` in the `server` directory.
    - Add the following variables, populating it with the specified credentials:
    `GITHUB_API_TOKEN="" OPENAI_API_KEY="" OPENAI_ORGANISATION_ID="" GOOGLE_API_KEY=""`.
    It is important to note that entering these configuration credentials is *optional*. However, by entering them all, the tool will be able to operate to its full potential.

3. **Create Virtual Environment `venv`**
    - Navigate to the `server` directory and run:
    `python -m venv venv`.

4. **Dependencies Installation**
    - Still in the `server` directory, execute:
    `pip install -r requirements.txt`.

### Client Configuration

1. **Dependencies Installation**
    - Navigate to the `client` directory and execute:
    `npm install`.

2. **Communication Port Configuration**
    - The React client, by default, connects to the Flask server on port `5000`.
    - If necessary, change the `proxy` variable in the `package.json` file in the `client` directory:
    `"proxy": "http://127.0.0.1:5000"`.

## Usage

### Server Startup

1. **Start the virtual environment `venv`**
    - Navigate to the `server` directory and execute:
    `venv\Scripts\activate`.

2. **Start the Flask server**
    - Still in the `server` directory, execute:
    `flask run`.
    Make sure the server is running on port `5000`.
    
### Client Startup

1. **Start the React client**
    - Navigate to the `client` directory and run:
    `npm start`.
    The application will start automatically in the default browser.


### Tool User Guide
Once the client and server are started, the web interface of ***TRACE*** can be accessed.

To analyse a repository:

1. Enter the repository in the input field using the `OWNER/NAME` format.
2. Click the `submit` button.
3. During processing, a loader will be shown. When processing is complete, detailed results or an error message will be shown.
4. The server `logs` can be consulted to monitor the processing.
___
# ITALIAN VERSION

## Indice
- [Introduzione](#introduzione)
- [Struttura Repository](#struttura-repository)
- [Requisiti di Sistema](#requisiti-di-sistema)
- [Installazione](#installazione)
  - [Configurazione Server](#configurazione-server)
  - [Configurazione Client](#configurazione-client)
- [Utilizzo](#utilizzo)
  - [Avvio Server](#avvio-server)
  - [Avvio Client](#avvio-client)
  - [Guida all'Uso del Tool](#guida-alluso-del-tool)

## Introduzione

Il tool ***TRACE***, sviluppato nell'ambito della mia Tesi di Laurea in Informatica presso l'Università degli Studi di Salerno, è progettato per analizzare le repository GitHub, con lo scopo principale di effettuare il calcolo della Dispersione Culturale in una comunità di sviluppatori. La sfida principale risiede nell'identificazione della Cultura di uno sviluppatore, a partire dalle limitate informazioni fornite da un account GitHub. Tale identificazione è fondamentale, poiché è utilizzata, successivamente, nel calcolo della Dispersione Culturale, mediante l'applicazione dell'Indice di Shannon.
Il tool è stato progettato con una struttura *client-server* sfruttando le potenzialità di due moderne tecnologie: `React` per il front-end e `Flask` per il back-end. Flask elabora le richieste sfruttando **formule matematiche**, **tecniche di Intelligenza Artificiale**, **cinque modelli predittivi** e **chiamate API** a servizio online per assicurare l'elaborazione di un risultato accurato.
Per maggiori approfondimenti si consiglia la lettura della <a href="https://github.com/cirovitale/TRACE/blob/main/thesis/CiroVitale_BachelorThesis_2023.pdf" target="_blank">Tesi</a>, in italiano.

## Struttura Repository
- directory `client`: client basato su React.
- directory `server`: server basato su Flask.
- directory `thesis`: Tesi di Laurea.

## Requisiti di Sistema
- **Memoria**: minimo 16 GB di RAM per supportare il caricamento in memoria del modello di ML.
- **Connessione Internet**: necessaria per le chiamate API. 

## Installazione

Effettuare il clone della repository.

### Configurazione Server

1. **Download e Configurazione Assets**
    - Scaricare l'archivio <a href="tinyurl.com/TRACE-ML-ASSETS" target="_blank">TRACE_ML_ASSETS</a> contenente le directory, `models` e `vectorizers`.
    - Trasferire le directory `models` e `vectorizers` nella directory `server`.

2. **Creazione file `.env`**
    - Creare un file denominato `.env` nella directory `server`.
    - Aggiungere le seguenti variabili, popolandolo con le credenziali specifiche:
        `GITHUB_API_TOKEN="" OPENAI_API_KEY="" OPENAI_ORGANIZATION_ID="" GOOGLE_API_KEY=""`.
    È importante notare che l'inserimento di tali credenziali è *facoltativo*. Tuttavia, inserendole tutte, il tool sarà in grado di operare al massimo delle potenzialità.

3. **Creazione Ambiente Virtuale `venv`**
    - Navigare fino alla directory `server` ed eseguire:
    `python -m venv venv`.

4. **Installazione Dipendenze**
    - Sempre nella directory `server`, eseguire:
    `pip install -r requirements.txt`.

### Configurazione Client

1. **Installazione Dipendenze**
    - Navigare fino alla directory `client` ed eseguire:
    `npm install`.

2. **Configurazione Porta di Comunicazione**
    - Il client React, di default, si connette al server Flask sulla porta `5000`.
    - Se necessario, modificare la variabile `proxy` nel file `package.json` nella directory `client`:
    `"proxy": "http://127.0.0.1:5000"`.

## Utilizzo

### Avvio Server

1. **Avviare l'ambiente virtuale `venv`**
    - Navigare fino alla directory `server` ed eseguire:
    `venv\Scripts\activate`.

2. **Avviare il server Flask**
    - Sempre nella directory `server`, eseguire:
    `flask run`.
    Assicurarsi che il server sia in esecuzione sulla porta `5000`.

### Avvio Client

1. **Avviare il client React**
    - Navigare fino alla directory `client` ed eseguire:
    `npm start`.
    L'applicazione verrà avviata automaticamente nel browser predefinito.

### Guida all'Uso del Tool
Una volta avviati client e server, è possibile accedere all'interfaccia web di ***TRACE***.

Per analizzare una repository:

1. Inserire la repository nel campo di input usando il formato `OWNER/NAME`.
2. Cliccare il pulsante `submit`.
3. Durante l'elaborazione, verrà mostrato un loader. Al termine dell'elaborazione, verranno mostrati i risultati dettagliati o un messaggio di errore.
4. I `log` del server possono essere consultati per monitorare il processo di elaborazione.



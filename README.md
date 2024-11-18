# Kezako
The **Recruit Me project** streamlines and automates the process of managing spontaneous job applications. It enables efficient tracking of applications sent, including the number of follow-up emails, response status, and key dates.

This automation is achieved by leveraging templates to generate personalized emails and cover letters, saving time and ensuring consistency in communication.

# Documentation
The current version of the CI is generating a documentation using sphinx and is accessible [`here`](https://arnaudsomville.github.io/recruit_me/)
There is still work to be done here as the documentation is really basic for now. 

# Installation

1. To setup the environnement, make sure to install miniconda https://docs.anaconda.com/miniconda/miniconda-install/
2. Create your python environnement
```
conda create -y -n my_env python=3.11
conda activate my_env
pip install pdm ruff=0.3.3 pre-commit
```
3. Go to your folder and install the packages using **pdm**. Initialize the project if needed
```
cd ~/your_work_folder
pdm install
```

# Use

## Configuration
After the pdm install, a new folder .recruit_me will be created in your home folder (if you delete it, it will be recreated each time the program is relaunched). A configuration file will be copied there from a template that you can find in [`src/recruit_me/configuration_template.yaml`](src/recruit_me/configuration_template.yaml)

You will have to put your informations there, the mecanisms permits to **avoid to commit personnal informations**.

## Run
This project is designed to be running on a distant server and to be controlled thanks to a restAPI that you can run with the following command :
```
uvicorn recruit_me.api.main_api:app --host 0.0.0
.0 --port 8100 --reload
```
Or running [`src/recruit_me/api/main_api.py`](src/recruit_me/api/main_api.py) (note that you can use the port you want)

The interface is accessible [`there`](http://localhost:8100/docs) (if you changed the port change it in the url)

## Templates

Templates in this context are customizable email or document structures where predefined placeholders are dynamically replaced with actual values during execution. This allows for generating personalized messages or documents efficiently, based on the provided data.

### Available Data Placeholders

- **`recipient_name`**: The name of the email recipient.  
  *Example*: `Elon Musk`

- **`recipient_email`**: The email address of the recipient.  
  *Example*: `elon.musk@spacex.com`

- **`recipient_company`**: The company the recipient is associated with.  
  *Example*: `SpaceX`

- **`recipient_position`**: The position or title of the recipient in their company.  
  *Example*: `CEO`

- **`sender_name`**: The name of the sender, usually preconfigured in the system's main configuration.  
  *Example*: `John Doe`

- **`sender_email`**: The sender's email address, sourced from the system configuration.  
  *Example*: `john.doe@example.com`

- **`current_date`**: The current date, formatted as `DD/MM/YYYY`.  
  *Example*: `13/11/2024`

### Example Template Usage

A sample email template might look like this:

```plaintext
Hello {{ recipient_name }},

I am {{ sender_name }}, and I wanted to reach out regarding a potential collaboration with {{ recipient_company }}.
```
When rendered with actual data, it would appear as:
```plaintext
Hello Elon Musk,

I am John Doe, and I wanted to reach out regarding a potential collaboration with SpaceX.
```

This structure makes templates versatile and reusable for different recipients or scenarios.

# Current Limitations
This project is still in developpement (it's been a long time I wanted to start it) so some features are still missing even if the main features are already working :
- For now, cover letter are not converted into pdf and are not pretty but an  [`issue`](https://github.com/arnaudsomville/recruit_me/issues/3) have been written to implement this functionality

- In the near future, the CI will be updated to automatically generate a docker image to deploy this software on a server and run it automatically

Don't hesitate to suggest improvements !

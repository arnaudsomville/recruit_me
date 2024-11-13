# Python base project

1. To setup the environnement, make sure to install miniconda https://docs.anaconda.com/miniconda/miniconda-install/
2. Create your python environnement
```
conda create -y -n my_env python=3.11
conda activate my_env
pip install pdm ruff=0.3.3 pre-commit
```
3. Go to your folder and install the packages. Initialize the project if needed

```
cd ~/your_work_folder
pdm init #Only if needed
pdm install
```
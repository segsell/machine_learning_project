[![Contributors][contributors-badge]][contributors-url]

# Machine Learning Project
Repository containing material for our machine learning project. 

## 1) Clone the Repository
Assuming you have already installed conda (if not, download the [conda package manager](https://docs.conda.io/en/latest/) first), 
open terminal (on MacOS and Ubuntu) or any other terminal emulator of your choice (e.g. [PowerShell](https://docs.microsoft.com/en-us/powershell/) on Windows, which - disclaimer - I have no personal experience with). Next, navigate to the folder where you want the repository to be downloaded. Then run

```console
$ git clone https://github.com/segsell/machine_learning_project.git
```


## 2) Activate *conda* Environment
Navigate to the folder containing the repository you just downloaded, e.g.

```console
$ cd Users/LMU_Munich/Winter_Semester_20_21/machine_learning_project
```

The file ``environment.yml`` lists a couple of basic packages for our project. 
These are the packages we also used in class to solve the problem sets.

To create and activate the *conda* environment run

```console
$ conda env create -f environment.yml
$ conda activate machine
```

The ```conda env create``` command only needs to be performed once. Whenever you work on the project, simply activate 
the ```machine``` environment before opening a jupyter notebook or working on a Python script (*.py* file). 
If you want to add any packages that are currently not listed in ``environment.yml``, add them to ``environment.yml``, navigate to the top-level directory of the project and run

```console
$ conda activate machine
$ conda env update -f environment.yml
```

## Contribution
Open terminal and navigate to the project folder. 
Make sure your local repository is up-to-date with the remote repository on GitHub. 
To do so, run

```console
$ git pull
```

which downloads all the latest contributions other team members have made on the remote repository.


If you have any data files, Python scripts or notebooks you want to upload, follow these steps.

Check which files you have added, modified or deleted

```console
$ git status
```

Then run

```console
$ git add <file>
$ git commit -m "<commit message>"
$ git push 
```

where ```<file>``` is the name of the file you want to upload, e.g. *reddit_data.csv* or *process_reddit_data.ipynb*,
and ```<commit message>``` is the message you include to describe what you did, which files you added, modified etc. 
For example, the message could read *"Add module sentiment_analysis"*.



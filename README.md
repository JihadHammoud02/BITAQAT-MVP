# Useful commands for git and Django

Some basic commands for Django, gitand github

## Django Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install Django==4.1.4
```

## Django Usage
### Run server:

```python
python manage.py runserver
```
### Create an application:

```python
Django-admin startapp app_name
```
#### P.S:
Whenever you make changes in the Django models (database), you need to migrate then apply migrations, you can find the commands down below
### Migrate:

```python
python manage.py migrate
```
### Apply migrations:

```python
python manage.py makemigrations
```


## Version control rules:
While working on version control, we need to set rules to follow for the sake of the team.
### 1-Branching:
Every feature you want to test  out without breaking the other part of the code , you can do that by creating a new branch from the most updated one and work on it, if everything goes well, you should inform you're colleagues that you will merge this branch with the newest one.
### 2-Branch naming convention:
```python
wip- What you are working on (ex: AuthSystem) - name (ex:wip-AuthSystem-Jihad)
```
### 3-Commits and push:
Whenever you created a mini part of the feature in your code you should add and commit the changes on your local git. After finishing this feature you will need first to pull the branch from github because some co-workers may have added some new code to the branch and pushed it out since your last pull.When you pull, the branch automatically will merge with your code locally, and then at this moment you can push it out to github.
## Git and github commands:
### Add :
```git
git add .
```
### Commit:
```git
git commit -m "commit name"
```

### Create branch:
```git
git checkout -b branch_name
```
### Switch to another branch:
```git
git checkout  branch_name
```
### Push to github:
First you need to make sure that a branch with the same name as your local branch already exists on github
```git
git push -u origin branch_name
```
### pull from branch:
```git
git pull -u origin branch_name
```
### Merge branches:
when you want to merge two branches, All you have to do is check out the branch you wish to merge into and then run the git merge command:
merging wip-AuthSystem-Jihad into master
```git
$ git checkout master
Switched to branch 'master'
$ git merge wip-AuthSystem-Jihad
```

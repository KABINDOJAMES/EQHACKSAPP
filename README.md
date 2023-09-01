# EQHACKSAPP
This is a platform whereby victims and users will be getting help by opening online tickets and advisors will be getting in touch with them through the contact details they give out.
> ## Steps to run the project are provided below

###LANDING PAGE
More images available on the demo-images folder.
![landing-page](https://github.com/KABINDOJAMES/EQHACKSAPP/assets/90185274/1a117828-f668-40ec-bbb8-8cbc7400d48e)


## Steps To Run The Project
> ## If you need any help, you can reach me at jameskalusimeon@gmail.com
The steps below make an assumption that you have:
 - [x] Python Installed In Your System
 - [x] Pip installed
 - [x] Virtual Environment

- Start By Cloning the project
```
git clone https://github.com/KABINDOJAMES/EQHACKSAPP.git
```
- Create a virtual environment for the project

   Example 
   ```
   virtualenv my_env
   ```
- Activate your virtual environment

   Example
   ```
   my_env\scripts\activate
   ```
 - Change the directory to your cloned repository
 - Install requirements by running
 ```
 pip install -r requirements.txt
 ```
 - Make Database Migrations
  ```
  python manage.py makemigrations
  ```
  Then
  ```
  python manage.py migrate
  ```
  - Create a super user 
   ```
   python manage.py createsuperuser
   ```
   Follow prompts and create a super user successfully to be able to log into the admin panel
   
   - Start Your web application at the local host 
   ```
   python manage.py runserver
   ```
   ### You Are Good To Go
   
   If Any Errors, Please leave a comment

# MathLab :triangular_ruler: :chart_with_upwards_trend:

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)![Python](https://img.shields.io/badge/python-3.11-orange)
![Gitea Forks](https://img.shields.io/github/forks/StanislavJPG/mathlab)

### The project is currently under development. It's not finished yet.
### **Math equations solver + Mathematical Q/A forum.** 
**Using:**

 :small_orange_diamond: **Django**

 :small_orange_diamond: **Django Rest Framework**

 :small_orange_diamond: **Django ORM (MySQL)**

 :small_orange_diamond: **Redis**

 :small_orange_diamond: **Elasticsearch**

 :small_orange_diamond: **BeautifulSoup**

----

## About this project
The main goal of this project is to provide help to the students and everyday people who want to 
improve their math skills.

---

### Installation

**From GitHub:**

```commandline
pip install https://github.com/StanislavJPG/mathlab.git
```

**Then install the project dependencies with**
```commandline
pip install -r requirements.txt
```

### Usage
**You can create your own .env file to optimize the project according to your preferences.**

```dotenv
SECRET_KEY=custom_secret_key

MAIL_NAME=your_mail

MAIL_PASS=your_smtp_app_pass

MYSQL_DB_PASS=your_mysql_pass

ELASTICSEARCH_HOST=elasticsearch_host

ELASTICSEARCH_NAME=elasticsearch_name

ELASTICSEARCH_PASS=elasticsearch_pass
```

**Now you can run the project using this command**

```commandline
python manage.py runserver
```

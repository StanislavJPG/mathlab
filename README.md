# MathLab :triangular_ruler: :chart_with_upwards_trend:

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)


## Math-related web-site

#### Here you can find:
- Solvers (You can automatically solve your math equations, marices, etc)
- Drafts (You can create your own mathematics drafts using drawing functionality and use it or share it with other theorists if you want!)
- GraphBuuilder (Build any graph that you want!)
- Forum (Fully math-integrated forum like stackoverflow.com or znanija.com)
- Chat (Share your achivements, posts, comments, drafts or just communicate with any theorist that you want in one place! Or just find new friends in math area!)


### About this project
The main goal of this project is to provide help to the students and everyday people who want to 
improve their math skills.

---

### Installation

**Copying project from GitHub:**

```commandline
git clone https://github.com/StanislavJPG/mathlab.git
```

* Create your own .env file by the .env.template in main directory.
* ```make up``` to create docker images and starts the containers.
* Open the second terminal for the ```make web``` command. It will run bash console.

**Then run in console:**
* ```./manage.py migrate``` - to apply all the migrations in DB.
* ```./manage.py loaddata post_categories``` - to create the categories in database.
* ```./manage.py load data mathlab_carousels``` - to create carousel info
* ```./manage.py createsuperuser``` - to create your own superuser (which is designed only for auth purposes).

After superuser creation make sure that you have registered 
directly from the site form to properly create your own `Theorist` model, which is related to `User`.

**NOTE:** You should grant admin permissions by selecting the `superuser status` checkbox for your recently registered user. The admin-panel URL path: `admin/`

#### And that's it! Now you can jump into it!

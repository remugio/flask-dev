cd-dev
===============================
CampusDebate Dev environment.

Tornado webserver wrapping Flask application. 

Integrates Flask, Tornado's websockets, and SockJS for graceful degradation

1. Install Vagrant (www.vagrantup.com)
2. Clone this repository. Navigate to its directory
3. Run 'vagrant up'
4. Navigate to http://localhost:8089 in your browser to view the tornado app

![Screenshot1](https://raw.githubusercontent.com/campusdebate/flask-tornado-websockets-sample/master/screenshot1.png)
![Screenshot2](https://raw.githubusercontent.com/campusdebate/flask-tornado-websockets-sample/master/screenshot2.png)


Dependencies
------------
 - Flask-0.10.1
 - Flask_MySQL-1.2
 - Flask_Bcrypt-0.6.0

DB Requirements
---------------
 - port = 3306
 - db/schema name = flaskr
 - db user = admin
 - db pw = default
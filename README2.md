# ArabicWikipedia
Lists all Wikipedia articles that have not been translated to Arabic

## Description
This is a script that parses Wikipedia and outputs the names of all the English articles that do not have an Arabic translation. This script was written in an effort to highlight articles that need to be translated for anyone who wants to contribute to increasing the Arabic content of the internet for the Arab users. This script work on GNU/Linux.

## Website
We are providing this script as an online tool to make it even easier to use. (LINK)[link]

## How to use
1. You need to install these dependencies for the script to work:

`sudo apt install python3-mysql.connector python3-tqdm mysql-server -y`

`sudo pacman -S python-mysql-connector python-tqdm mariadb`

The command depends on your linux distribution.

2. Setup a MYSQL server (knowlege of how to use and setup MySQL will help you bypass any unforseen issues):

`
mysql -u root -p
use mysql;
create user 'alroot'@'localhost' identified by '';
grant all privileges on *.* to 'alroot'@'localhost';
UPDATE user SET plugin='mysql_native_password' WHERE User='alroot';
flush privileges;
exit;
service mysql restart
`

3. To download the wikipedia database (~2GB download and ~6GB uncompressed):

`python wiki.py download`

4. To parse the database, there is no password (~5 hours):

`python wiki.py parse`

5. To run the analysis:

`python wiki.py run`
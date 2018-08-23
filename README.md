# non-translated-wiki
English wikipedia pages that doesnt have been translated to arabic


first time you have to run install.py file to instal dependencies (modules: mysql and tqdm) 
then you can run wiki.py.
it will create new folder "sql" then it will download two big sql files (1GB+) each, so it may take very long time to setup app for the first time (time depend on your machine).


*you can get the same result of this program by working with mysql manually as following:-*


    

1- download sql files from Wikimedia : 
( https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-langlinks.sql.gz )
( https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-page.sql.gz )

2- install mysql

    $sudo apt-get mysql install
  
3- create database :

    $mysql -u <username> -p
    
    example:
    $mysql -u root -p
    (enter your password, if no password just press enter)
    
    mysql> CREATE DATABASE IF NOT EXISTS wiki;
    
4- import sql files to that database : 
    
    $mysql -u username -p databasename < filename.sql 
    
    example:
    $mysql -u root -p wiki < enwiki-latest-langlinks.sql

5- create new database table to store only arabic translation linkes:

    mysql> CREATE TABLE IF NOT EXISTS `langlinks_ar` ( `ll_from` int(8) UNSIGNED NOT NULL DEFAULT '0',  `ll_lang` varbinary(20) NOT NULL,  `ll_title` varbinary(255) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;

6- get only arabic links from 'langlinks' (table which we imported from step 4) then store it in 'langlinks_ar' table which we created in step 5:

    mysql>INSERT INTO `langlinks_ar`(`ll_from`, `ll_lang`, `ll_title`) SELECT * FROM langlinks WHERE ll_lang = 'ar';

7- optional : delete langlinks table which contains all other languages links:

    mysql> DROP TABLE langlinks;
    
8- show all titles from wikipedia pages where it has not translated to arabic:

    mysql> SELECT CAST(page_title as CHAR) FROM page inner join langlinks_ar ON langlinks_ar.ll_from != page.page_id ;

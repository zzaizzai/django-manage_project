# how-to-install-this-project

## python-install

### download-python

- https://www.python.org/downloads/

### set-python-path 

system environmental variables
PYTHONHOME : C:\Users\junsa\AppData\Local\Programs\Python\Python39
PYTHONPATH : D:\manage_project\venv\Lib\site-packages

### mod_wsgi

- if yout use python3.9 64bit, download *cp39-amd64.whl

https://www.lfd.uci.edu/~gohlke/pythonlibs/#mod_wsgi

- move wsgi file to manage_project dir

### pip-install

- if there are some error installing mod_wsgi, update pip to new version
- pip install mod-wsgi


## postgresql-install

### download-sql
- https://www.postgresql.org/download/


## apache-install

### download-apahce
- https://www.apachelounge.com/download/
- dowload `httpd-2.4.xx-win64.zip`
- unzip

### setting

- copy Apache24 dir to C:\

```termial
cd C:\Apache24\bin
httpd -k install
```

- open `Apahce24/conf/httpd.conf`` and add lines like this

```
LoadFile "C:\Users\junsa\AppData\Local\Programs\Python\Python39\python39.dll"
LoadModule wsgi_module D:\manage_project\venv\Lib\site-packages\mod_wsgi\server\mod_wsgi.cp39-win_amd64.pyd

WSGIPythonHome D:\manage_project\venv
WSGIPythonPath D:\manage_project

WSGIScriptAlias / D:\manage_project\manage_project\wsgi.py

<Directory D:\manage_project\manage_project>
    <Files wsgi.py>
        Require all granted
    </Files>
</Directory>

Alias /static D:\manage_project\static

<Directory D:\manage_project\static>
    Require all granted
</Directory>
```

### start-apahce

- check `127.0.0.1:80/admin`
# Backend

### Environment Setting
(1) Create your virtual environment

(2) Install requirements
```
pip install -r requirements.txt
```

(3) Download the mysql from the homepage. (https://dev.mysql.com/downloads/windows/installer/)

(4) Write the *.env* file according to your database setup

- example *.env* file
    ```
    MYSQL_HOST= your_host
    MYSQL_USER= your_user
    MYSQL_PASSWORD= your_password
    SQLALCHEMY_DATABASE_URL = mysql+pymysql://your_user:your_password@your_host/kanbu
    ```

(5) Make new Database and Insert sample data into a database

``` 
python insert_table.py
```

(6) Run the Server

``` 
uvicorn main:app --reload
```
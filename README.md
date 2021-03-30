# CSE4550-GroupProject
Repo for Spring 2021 CSE 4550 

Install Flask using terminal (I am using Ubuntu Linux)
    
    pip install flask

Start Flask Server from project folder:
    
    export FLASK_APP=dealership.py

    Windows:
    set FLASK_APP=dealership.py

Debug mode:
    export FLASK_DEBUG=1

    Windows:
    set FLASK_DEBUG=1

Run application:
    
    flask run

    NOTE: the default local IP did not work for me. I had to use: flask run --host 0.0.0.0. It will make the server externally visible. If the IP address of the machine is 192.168.X.X then, from the same network you can access it in 5000 port. So only do the 0.0.0.0 on trusted network.

    Open browser and goto: 
        http://127.0.0.1:5000/

    Or if used 0.0.0.0:5000 go to that one should see "Hello World"

    # Flask Bootstrap Reference: use after initial Hello World install

    [Link to tutorial ](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates)
 
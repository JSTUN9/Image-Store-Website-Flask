from website import create_app #from website folder, import create_app which was defined in the website pacakge

app = create_app()

if __name__ == '__main__': # only if we run main.py, and not import it, that we will run the next line of code (which is running the webserver)
    app.run(debug=True) #debug=True means if we make any change in the code, the web server will rerun

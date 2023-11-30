from app import app

if __name__ == "__main__":
    from gunicorn.app.wsgiapp import WSGIApplication

    sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
    sys.exit(WSGIApplication().run())

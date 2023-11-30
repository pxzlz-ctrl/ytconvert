from your_app_module import app

if __name__ == "__main__":
    import os
    import sys
    from gunicorn.app.wsgiapp import WSGIApplication

    sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
    sys.exit(WSGIApplication().run())

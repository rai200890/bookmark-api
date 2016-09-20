from bookmark_api import app, db


@app.route("/healthcheck")
def healthcheck():
    result = db.engine.execute("SELECT 1;").fetchone()
    return "DB: OK {}".format(result)

if __name__ == "__main__":
    app.run()

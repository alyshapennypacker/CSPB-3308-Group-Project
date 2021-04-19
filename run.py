from flaskapp import app, db
from flaskapp.tests.db_tables import bootstrap_helper, query_helper

@app.cli.command("init-db")
def reset_db():
    ''' Drops and Creates fresh database '''
    db.drop_all()
    db.create_all()
    print("Initialized clean DB tables")


@app.cli.command("load-db")
def bootstrap_data():
    ''' Populates database with some sample data '''
    db.drop_all()
    db.create_all()
    bootstrap_helper(db)
    print("Loading data...\n")
    print("Re-Initialized DB and Bootstrapped with sample data")

@app.cli.command("query-db")
def query_sampleData():
    ''' Queries sample data from `boot` command '''
    query_helper(db)
    print("Querying Sample Data...")


if __name__ == '__main__':
    app.run(debug=True)
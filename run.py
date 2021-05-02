from flaskapp import create_app

from flaskapp import db
from flaskapp.tests.db_tables import bootstrap_helper, query_helper

app = create_app()
app.app_context().push()

@app.cli.command("db-clean")
def reset_db():
    ''' Drops and Creates fresh database '''
    db.drop_all()
    db.create_all()
    print("Initialized clean DB tables")


@app.cli.command("db-load")
def bootstrap_data():
    ''' Populates database with some sample data '''
    db.drop_all()
    db.create_all()
    bootstrap_helper(db,app)
    print("Loading data...\n")
    print("Re-Initialized and Bootstrapped with sample data")


@app.cli.command("db-query")
def query_sampleData():
    ''' Queries sample data from `boot` command '''
    with app.app_context():
        query_helper(db,app)
        print("Querying Sample Data...")


if __name__ == '__main__':
    app.run(debug=True)

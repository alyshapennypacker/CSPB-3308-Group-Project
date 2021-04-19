from .app import app, db


@app.cli.command("initdb")
def reset_db():
    ''' Drops and Creates fresh database '''
    db.drop_all()
    db.create_all()
    print("Initialized clean DB tables")


@app.cli.command("bootstrap")
def bootstrap_data():
    ''' Populates database with some sample data '''
    db.drop_all()
    db.create_all()
    # bootstrap_helper()
    print("Initialized clean DB tables and Bootstrapped with data")

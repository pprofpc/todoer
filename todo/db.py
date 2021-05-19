import mysql.connector

import click #ejecuta comandos en la terminal
from flask import current_app, g #g es una variable Global, nosotros la utilizamos para almacenar el usurio
from flask.cli import with_appcontext #sirve para acceder a las variables que se encuentran en la configuración de la aplicación
from .schema  import instructions #va a tener los script necesarios para crear nuestra DB

def get_db():
    if 'db' not in g:
        g.db= mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)

    db.commit()

@click.command('init-db') #Nombre que voy a utilizar desde la terminal con flask
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Base de datos inicializada')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

 

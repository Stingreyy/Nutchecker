from flask_migrate import Migrate
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from app import create_app, db

app = create_app()
migrate = Migrate(app, db)

# Lägg till Server-command för att köra appen
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server())

if __name__ == '__main__':
    manager.run()

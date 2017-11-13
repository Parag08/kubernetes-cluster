import os
from cluster_management import app
from cluster_management.core import db


def runserver():
    port = int(os.environ.get('PORT', 5000))
    db.create_all()
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    runserver()


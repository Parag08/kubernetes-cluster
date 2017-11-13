from flask import Flask

app = Flask(__name__)

app.config.from_object('cluster_management.settings')

import cluster_management.core
import cluster_management.src.user_manager
import cluster_management.src.resource_manager
import cluster_management.backdoor

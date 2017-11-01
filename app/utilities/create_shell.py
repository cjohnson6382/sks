import os
import sys

sys.path.append(os.getcwd())

import json

from app import create_app, db

# from project.models import RoleHolder, App, Asset, IdTranslation, Organization, Point, RoleHolder, Schema, Site, Transaction, User # Installed, 
from app.models import User, Organization, Inspection, Assigned, Completed, Contractor, Data, Learning, Site

app = create_app("development")
app_context = app.app_context()
app_context.push()
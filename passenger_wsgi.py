import sys, os

# Add the project directory to the sys.path
# This is usually required for cPanel/Hostinger Python apps to find your modules
sys.path.append(os.getcwd())

from app import app as application

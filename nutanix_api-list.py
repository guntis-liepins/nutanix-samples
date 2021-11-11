#!/usr/bin/env python3
import sys 
import os
import json
from requests import Response
from nutanixapi.nutanixapi import NutanixAPI
import logging  
from getpass import getpass


URL="" #Prism API URL
#-----------------------------------------------------------------------------

username=input("Nutanix username:")
password=getpass("Nutanix password:")
max_results=99999       #limits maximum results. Not needed for small installs.
api=NutanixAPI(URL,username,password,"/tmp/nutanix_api.log",logging.DEBUG,False)


print("### CLUSTERS ###")
api.list_clusters_screen() #list subnets
print("### SUBNETS ###")
api.list_subnets_screen() #list subnets
print("### IMAGES ###")
api.list_images_screen() #list images
print("### PROJECTS ###")
api.list_projects_screen() #list-projects
print("### VMS ###")
api.list_vms_screen()

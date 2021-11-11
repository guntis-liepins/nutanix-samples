#!/usr/bin/env python3
import sys
import os
import json
import time
from requests import Response
from nutanixapi.nutanixapi import NutanixAPI
import logging
from getpass import getpass
from pathlib import Path

DBG=True
#LOG_FILE="c:\\temp\\nutanix_api.log" #windows
LOG_FILE="/tmp/nutanix_api.log" #linux

def main():

    URL="" #Prism Central URL
    vm_uuid=""  #UUID of VM to work with

    username=input("Nutanix username:")
    password=getpass("Nutanix password:")
    
    api=NutanixAPI(URL,username,password,LOG_FILE,logging.DEBUG,False)
    
    #poweron test
    # poweron_response=api.vm_poweron(vm_uuid)
    # (poweron_status_code,poweron_result_json)=api.process_response(poweron_response)
    # api.continue_if_ok(poweron_status_code,"ERROR: VM power ON call failed")
    # poweron_task_uuid=api.get_task_uuid(poweron_result_json)
    # poweron_task_status=api.wait_for_task(poweron_task_uuid)
    # api.continue_if_task_ok(poweron_task_status,"poweron task failed")

    #poweroff test
    poweron_response=api.vm_poweroff(vm_uuid)
    (poweron_status_code,poweron_result_json)=api.process_response(poweron_response)
    api.continue_if_ok(poweron_status_code,"ERROR: VM power ON call failed")
    poweron_task_uuid=api.get_task_uuid(poweron_result_json)
    poweron_task_status=api.wait_for_task(poweron_task_uuid)
    api.continue_if_task_ok(poweron_task_status,"poweron task failed")

    sys.exit(0) #great success

    
if __name__ == "__main__":
    main()

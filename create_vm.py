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

DBG=True    #print debug info if True
#LOG_FILE="c:\\temp\\nutanix_api.log" #windows
LOG_FILE="/tmp/nutanix_api.log" #linux

def main():
    current_path = Path(__file__).parent.resolve()
    # directory where a three cloud-init templates are located
    # - templates/cloud-init-net.yaml.j2
    # - templates/cloud-init.yaml.j2
    # - templates/static.yaml.j2
    template_dir=os.path.join(current_path,"templates")
    URL=""

    username=input("Nutanix username:")
    password=getpass("Nutanix password:")

    api=NutanixAPI(URL,username,password,LOG_FILE,logging.DEBUG,False)

    #data required for vm creation
    cluster_uuid="" #UUID of cluster
    subnet_uuid=""  #UUID of subnet
    project_uuid="" #UUID of project
    image_uuid=""   #UUID of image
    owner_uuid=api.get_current_user_uuid()

    vm_name=""    #Name of VM
    vm_dns=""     #DNS name of VM
    vm_ip=""      #VM IP , optional
    vm_description="" #description of VM
    sockets=1
    vcpu_per_socket=1
    thread_per_core=1
    memory_mb=1024  #memory in megabytes
    disk_size='30G' #disk size in human readable format


    #create VM
    print("Creating VM")

   #  There are three cases in Nutanix:
   #              network_cfg = None
   #                            Assign ip address automatically DHCP. 
   #                            Must be used by only on networks managed by nutanix.
   #              network_cfg (String) = ip_address
   #                            Assign specified ip_address. 
   #                            Sets specified IP address using Nutanix. Netmask and gatway is 
   #                            inherited from network definition 
   #                            Must be used by networks managed by nutanix,otherwise it will fail.
   #                            (with error Cannot assign IP address in unmanaged network)
   #              network_cfg (Dictionary) = 
   #                              { ip_address  (String)
   #                                prefix (String)
   #                                default_gw (String)
   #                                dns_server1 (String)
   #                                dns_server2 (String)   
   #                                dns_search  (String)
   #                              }
   #                             Sets network according to dictionary.
   #                             Must be used for networks not managed by Nutanix 


    response=api.create_vm_simple(
                    vm_name=vm_name,
                    vm_description=vm_description,
                    cluster_uuid=cluster_uuid,
                    project_uuid=project_uuid,
                    owner_uuid=owner_uuid,
                    source_image_uuid=image_uuid,
                    subnet_uuid=subnet_uuid,
                    num_threads_per_core=thread_per_core,
                    num_vcpus_per_socket=vcpu_per_socket,
                    num_sockets=sockets,
                    memory_size_mib=memory_mb,
                    template_dir=template_dir,
                    network_cfg=None
                    )
                        
    (status_code,result_json)=api.process_response(response)
    api.continue_if_ok(status_code,"ERROR: vm creation call failed")
    vm_uuid=result_json['metadata']['uuid']
    if DBG: print(f"VM UUID:{vm_uuid}")
    task_uuid=api.get_task_uuid(result_json)
    if DBG: print(f"Task UUID:{task_uuid}")
    task_status=api.wait_for_task(task_uuid)
    api.continue_if_task_ok(task_status,"ERROR: vm creation task failed!")
    print(f"VM created UUID:{vm_uuid}")

 #now resize VM disk to desired size
    print("Resizing disk")
    disk0_uuid=api.get_disk0(vm_uuid)
    if DBG: print(f'Disk0 UUID:{disk0_uuid}')
    if DBG: print(f"Resizing disk {disk0_uuid} to {disk_size}")
    response_resize=api.resize_vm_disk(vm_uuid,disk0_uuid,disk_size)
    (resize_status_code,resize_result_json)=api.process_response(response_resize)
    api.continue_if_ok(resize_status_code,"ERROR: disk resize call failed")
    resize_task_uuid=api.get_task_uuid(resize_result_json)
    print(f"resize task uuid:{resize_task_uuid}")
    resize_task_status=api.wait_for_task(api,resize_task_uuid)
    api.continue_if_task_ok(resize_task_status,"rdisk resize task failed")

    # now powering on VM
    print(f"Powering on VM {vm_uuid}")
    poweron_response=api.vm_poweron(vm_uuid)
    (poweron_status_code,poweron_result_json)=api.process_response(poweron_response)
    api.continue_if_ok(poweron_status_code,"ERROR: VM power ON call failed")
    poweron_task_uuid=api.get_task_uuid(poweron_result_json)
    poweron_task_status=api.wait_for_task(api,poweron_task_uuid)
    api.continue_if_task_ok(poweron_task_status,"poweron task failed")
To use samples clone sample github repository https://github.com/guntis-liepins/nutanix-samples.git

```
git clone https://github.com/guntis-liepins/nutanix-samples.git
```

Change to this directory and then create and activate python virtualenv in venv folder
(naming it venv can help Visual Studio code to work with virtualenv)
```
ctrlz@vulcan:~/Projects/Python$ cd nutanixapi-samples
ctrlz@vulcan:~/Projects/Python/nutanixapi-samples$ python3 -m venv venv
ctrlz@vulcan:~/Projects/Python/nutanixapi-samples$ source venv/bin/activate
```

First install wheel to be able to install nutanix packages from source.
This is due unsolved bug - wheel installs after nutanixapi so nutanixapi install will fail.
Need to be done only once when new virtualenv is created.
```
pip install wheel
```
There are requirements.txt file which contain nutanixapi repository as requiement.
Install nutanixapi using this file.

```
pip install wheel
pip install -r requirements.txt
```

In nutanix-samples repo are directory cloud-init-samples which contain cloud-init-templates for different types of networks.
copy directory to templates
```
cp -r cloud-init-samples templates
```
Then REPLACE all marked data with own values in cloud init files

Scripts:
    - nutanix_api-list.py - You can test functionality of nutanixapi by running script nutanix_api-list.py and find out UUIDs of objects
    - create_vm.py - example how to create VM
    - power.py - example how to power on and off VM







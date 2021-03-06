#!/usr/bin/env python
import urllib2
import urllib
import json
import pprint

# Put the details of the dataset we're going to create into a dict.


dataset_list = [{
    'name': 'my_dataset_name3',
    'notes': 'A long description of my dataset',
    'owner_org': 'cartong',
    'url':'url',#requiered
},{
    'name': 'my_dataset_name4',
    'notes': 'A long description of my dataset',
    'owner_org': 'cartong',
    'url':'url2',#requiered
}
]

# Use the json module to dump the dictionary to a string for posting.
for dataset_dict in dataset_list :
   print dataset_dict
   data_string = urllib.quote(json.dumps(dataset_dict))
   
   # We'll use the package_create function to create a new dataset.
   request = urllib2.Request(
       'http://datasources.cartong.org/api/action/package_create')
   
   # Creating a dataset requires an authorization header.
   # Replace *** with your API key, from your user account on the CKAN site
   # that you're creating the dataset on.
   request.add_header('Authorization', '98ba290a-bce8-4f5a-9f43-dba29115b6e5')
   
   # Make the HTTP request.
   response = urllib2.urlopen(request, data_string)
   assert response.code == 200
   
   # Use the json module to load CKAN's response into a dictionary.
   response_dict = json.loads(response.read())
   assert response_dict['success'] is True
   
   # package_create returns the created package as its result.
   created_package = response_dict['result']
   pprint.pprint(created_package)
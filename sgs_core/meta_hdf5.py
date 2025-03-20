# Reading and writing HllSets from and to hdf5
#
# In this exercise, you will implement the store_hllset and retrieve_hllset methods in the 
# HDF5Store class in sgs_core/meta_hdf5.py. The store_hllset method should store an HllSet 
# in an HDF5 file, and the retrieve_hllset method should retrieve an HllSet from an HDF5 file. 
# You will use the HllSet class from sgs_core/meta_algebra.py to represent the HllSet in Python.

import h5py
from meta_algebra import HllSet
import requests

class HDF5Store:
    def __init__(self, file_path="data.h5"):
        """
        Initialize the HDF5Store with a file path.
        """
        if file_path == None:
            file_path = "data.h5"
        elif not file_path.endswith(".h5"):
            raise ValueError("File path must end with '.h5'")
        self.file_path = file_path

    def store_hllset(self, key, hllset):
        """
        Store an HllSet in the HDF5 file.
        """
        with h5py.File(self.file_path, 'a') as f:
            group = f.require_group("hllsets")
            if key in group:
                del group[key]  # Delete existing dataset if it exists
            dataset = group.create_dataset(key, data=hllset.hll.counts)

    def retrieve_hllset(self, key, P=10):
        """
        Retrieve an HllSet from the HDF5 file.
        """
        with h5py.File(self.file_path, 'r') as f:
            group = f.get("hllsets")
            if group is None or key not in group:
                return None
            counts = group[key][:]
            hllset = HllSet(P)
            hllset.hll.counts = counts
            return hllset
        
    def call_hdf5():
        try:
            # Make a GET request to the hdf5 service
            response = requests.get("http://hdf5:5000/read")  # Replace "/endpoint" with the actual endpoint of your Flask app
            
            # Check if the request was successful
            if response.status_code == 200:
                return {"status": "success", "data": response.json()}
            else:
                return {"status": "error", "message": f"HTTP {response.status_code}: {response.text}"}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}

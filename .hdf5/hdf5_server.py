import h5py
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Path to the HDF5 file
HDF5_FILE_PATH = "data.h5"

def create_demo_file():
    """Create a dummy HDF5 file if it doesn't exist."""
    if not os.path.exists(HDF5_FILE_PATH):
        with h5py.File(HDF5_FILE_PATH, "w") as f:
            f.create_dataset("demo_dataset", data=[1, 2, 3, 4, 5])
        print(f"Created demo HDF5 file at {HDF5_FILE_PATH}")

@app.route('/read', methods=['GET'])
def read_hdf5():
    file_path = request.args.get('file', HDF5_FILE_PATH)  # Use default file if not provided
    dataset = request.args.get('dataset', "demo_dataset")  # Use default dataset if not provided
    try:
        with h5py.File(file_path, 'r') as f:
            if dataset not in f:
                return jsonify({"error": f"Dataset '{dataset}' not found in file"}), 404
            data = f[dataset][:]
        return jsonify(data.tolist())
    except FileNotFoundError:
        return jsonify({"error": f"File '{file_path}' not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/write', methods=['POST'])
def write_hdf5():
    file_path = request.args.get('file', HDF5_FILE_PATH)  # Use default file if not provided
    dataset = request.args.get('dataset', "demo_dataset")  # Use default dataset if not provided
    data = request.json.get('data')
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        with h5py.File(file_path, 'a') as f:
            if dataset in f:
                del f[dataset]  # Delete existing dataset if it exists
            f.create_dataset(dataset, data=data)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Create a demo file if it doesn't exist
    create_demo_file()
    # Start the Flask server
    app.run(host='0.0.0.0', port=5000)
FROM python:3.12-slim
RUN apt-get update && apt-get install -y libhdf5-dev
WORKDIR /app
COPY hdf5_server.py .
COPY data.h5 .
RUN pip install h5py flask
CMD ["python3", "hdf5_server.py"]
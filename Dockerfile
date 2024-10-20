# Gunakan image dasar Apache Airflow
FROM apache/airflow:2.10.2

# Set direktori kerja
WORKDIR /opt/airflow

# Salin file requirements.txt ke dalam container
COPY requirements.txt .

# Ubah ke pengguna root untuk menginstal paket
USER root

# Install dependencies yang dibutuhkan, termasuk OpenCV
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-opencv \
        cmake \
        ninja-build

# Kembali ke pengguna airflow
USER airflow

# Atur perintah default untuk container
CMD ["airflow", "webserver"]

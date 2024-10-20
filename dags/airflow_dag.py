# airflow_dag.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import cv2
import os

default_args = {
    'owner': 'user',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

def extract_video(video_path):
    """Extract video file"""
    # Check if video file exists
    if not os.path.exists(video_path):
        raise Exception(f"{video_path} does not exist!")
    return video_path

def transform_video_to_frames(video_path, output_dir):
    """Transform video into frames"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the video file using OpenCV
    video_capture = cv2.VideoCapture(video_path)
    frame_count = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        # Save each frame as an image
        frame_filename = os.path.join(output_dir, f"frame_{frame_count}.jpg")
        cv2.imwrite(frame_filename, frame)
        frame_count += 1
    
    video_capture.release()
    return output_dir

def load_frames_to_folder(output_dir):
    """Just a placeholder function to simulate loading data"""
    print(f"All frames saved to {output_dir}")
    return output_dir

with DAG(dag_id='video_etl', default_args=default_args, schedule_interval='@daily') as dag:
    filename = "happy.mp4"
    data_type = "happy"
    data_source = f"./data/raw/{filename}"
    data_dest = f"./data/transformed/{data_type}"
    
    # Step 1: Extract video
    extract = PythonOperator(
        task_id='extract_video',
        python_callable=extract_video,
        op_kwargs={'video_path': data_source},
    )

    # Step 2: Transform video to frames
    transform = PythonOperator(
        task_id='transform_video_to_frames',
        python_callable=transform_video_to_frames,
        op_kwargs={'video_path': data_source, 'output_dir': data_dest},
    )

    # Step 3: Load the frames
    load = PythonOperator(
        task_id='load_frames',
        python_callable=load_frames_to_folder,
        op_kwargs={'output_dir': data_dest},
    )

    extract >> transform >> load

import os
import requests
from roboflow import Roboflow

class RoboflowUploader:
    def __init__(self, workspace, project, api_key, labeler_email, reviewer_email):
        self.WORKSPACE = workspace
        self.PROJECT = project
        self.ROBOFLOW_API_KEY = api_key
        self.LABELER_EMAIL = labeler_email
        self.REVIEWER_EMAIL = reviewer_email
        self.job_info = {}  # Initialize job_info as an instance variable

        self.rf = Roboflow(api_key=self.ROBOFLOW_API_KEY)
        self.upload_project = self.rf.workspace(self.WORKSPACE).project(self.PROJECT)

    def upload_images(self, folder_path):
        if not os.path.exists(folder_path):
            print(f"Folder '{folder_path}' does not exist.")
            return

        for image_name in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_name)

            if os.path.isfile(image_path):
                print('Image path:', image_path)

                response = self.upload_project.upload(image_path, batch_name='intelbatchtest', tag_names=['RE005'])
                print(image_path, response)

    def extract_batches(self):
        url = f"https://api.roboflow.com/{self.WORKSPACE}/{self.PROJECT}/batches"
        headers = {"Authorization": f"Bearer {self.ROBOFLOW_API_KEY}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            batch = response.json()
            print(batch)
            for batch in batch['batches']:
                self.job_info[batch['id']] = batch['images']  # Store job_info as an instance variable
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

    def assign_jobs(self):
        url = f"https://api.roboflow.com/{self.WORKSPACE}/{self.PROJECT}/jobs"
        headers = {
            "Content-Type": "application/json",
        }

        for job_id in self.job_info.keys():
            data = {
                "name": "Job created by API",
                "batch": job_id,
                "num_images": self.job_info[job_id],
                "labelerEmail": f"{self.LABELER_EMAIL}",
                "reviewerEmail": f"{self.REVIEWER_EMAIL}",
            }
            params = {
                "api_key": self.ROBOFLOW_API_KEY,
            }

            response = requests.post(url, headers=headers, json=data, params=params)

            if response.status_code == 200:
                print("Job created successfully!")
            else:
                print(f"Error occurred: {response.status_code} - {response.text}")


if __name__ == "__main__":
    uploader = RoboflowUploader(
        workspace="workspace_name",
        project="project_name",
        api_key="api_key",
        labeler_email="labeler_email",
        reviewer_email="reviewer_email"
    )

    uploader.upload_images("rivereye005_cam1_data")
    uploader.extract_batches()
    uploader.assign_jobs()

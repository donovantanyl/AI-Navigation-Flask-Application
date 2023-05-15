import roboflow
import os


class RoboflowAPI:
    def __init__(self, api_key):
        self.__project = None
        self.__rf = roboflow.Roboflow(api_key=api_key)

    def get_projects(self):
        return self.__rf.workspace().projects()

    def set_project(self, project_id):
        self.__project = self.__rf.workspace().project(project_id)
        return

    def upload_image(self, folder_dir):
        if self.__project:
            for images in os.listdir(folder_dir):
                if images.endswith(".jpg"):
                    self.__project.upload(f"{folder_dir}\\{images}")


rbf_api = RoboflowAPI(api_key="DPbpbi8dRt3gmUJZLKAd")

print(rbf_api.get_projects())

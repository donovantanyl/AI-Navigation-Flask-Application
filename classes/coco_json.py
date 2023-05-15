import datetime

now = datetime.datetime.now()


class COCO:
    def __init__(self, images, annotations):
        self.__info = {
            "year": now.year,
            "version": "10",
            "description": "Exported from WK Python Script",
            "contributor": "",
            "url": "https://public.roboflow.ai/object-detection/undefined",
        }
        self.__licenses = [
            {
                "id": 1,
                "url": "https://creativecommons.org/licenses/by/4.0/",
                "name": "CC BY 4.0"
            }
        ]
        self.__categories = [{"id": 0, "name": "Numbers", "supercategory": "none"},
                             {"id": 1, "name": "0", "supercategory": "Numbers"},
                             {"id": 2, "name": "1", "supercategory": "Numbers"},
                             {"id": 3, "name": "2", "supercategory": "Numbers"},
                             {"id": 4, "name": "3", "supercategory": "Numbers"},
                             {"id": 5, "name": "4", "supercategory": "Numbers"},
                             {"id": 6, "name": "5", "supercategory": "Numbers"},
                             {"id": 7, "name": "6", "supercategory": "Numbers"},
                             {"id": 8, "name": "7", "supercategory": "Numbers"},
                             {"id": 9, "name": "8", "supercategory": "Numbers"},
                             {"id": 10, "name": "9", "supercategory": "Numbers"},
                             {"id": 11, "name": "A", "supercategory": "Numbers"},
                             {"id": 12, "name": "Bus", "supercategory": "Numbers"},
                             {"id": 13, "name": "E", "supercategory": "Numbers"},
                             {"id": 14, "name": "G", "supercategory": "Numbers"},
                             {"id": 15, "name": "M", "supercategory": "Numbers"},
                             {"id": 16, "name": "W", "supercategory": "Numbers"},
                             {"id": 17, "name": "e", "supercategory": "Numbers"}]

        self.__images = images
        self.__annotations = annotations

    def return_json(self):
        output = {
            "info": self.__info,
            "licenses": self.__licenses,
            "categories": self.__categories,
            "images": self.__images,
            "annotations": self.__annotations
        }

        return output


class Image:
    def __init__(self, id, file_name, height, width):
        self.__id = id
        self.__file_name = file_name
        self.__height = height
        self.__width = width
        self.__date_captured = now.isoformat()

    def return_json(self):
        output = {
            "id": self.__id,
            "license": 1,
            "file_name": self.__file_name,
            "height": self.__height,
            "width": self.__width,
            "date_captured": self.__date_captured
        }
        return output


class Annotation:
    def __init__(self, id, image_id, category_id, bbox):
        self.__id = id
        self.__image_id = image_id
        self.category_id = category_id
        self.__bbox = bbox
        self.__area = bbox[2] * bbox[3]

    def return_json(self):
        output = {
            "id": self.__id,
            "image_id": self.__image_id,
            "category_id": self.category_id + 1,
            "bbox": self.__bbox,
            "area": self.__area,
            "segmentation": [],
            "iscrowd": 0
        }
        return output

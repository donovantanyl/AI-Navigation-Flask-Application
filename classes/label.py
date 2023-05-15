import json
import uuid


class Label:
    def __init__(self, label, conf, xyxy, width, height):
        self.__label = label
        self.__conf = conf
        self.__x1 = float(xyxy[0])  # x-min
        self.__y1 = float(xyxy[1])  # y-min
        self.__x2 = float(xyxy[2])  # x-max
        self.__y2 = float(xyxy[3])  # y-max
        self.__width = width  # width of image
        self.__height = height  # height of image

    def get_label(self):
        return self.__label

    def get_conf(self):
        return self.__conf

    def get_x1(self):
        return self.__x1

    def get_y1(self):
        return self.__y1

    def get_x2(self):
        return self.__x2

    def get_y2(self):
        return self.__y2

    def get_json(self):
        json_id = uuid.uuid4().hex
        label_json = {
            "id": json_id,
            "type": "rectanglelabels",
            "from_name": "label",
            "to_name": "image",
            "original_width": self.__height,
            "original_height": self.__width,
            "image_rotation": 0,
            "value": {
                "rotation": 0,
                "x": self.__x1 / self.__height * 100,
                "y": self.__y1 / self.__width * 100,
                "width": (self.__x2 - self.__x1) / self.__height * 100,
                "height": (self.__y2 - self.__y1) / self.__width * 100,
                "rectanglelabels": [self.__label]
            }
        }
        return label_json


def json_result(list_json, image_data):
    result = {
        "data": {
            "image": image_data
        },
        "predictions": [
            {
                "model_version": "one",
                "score": 0.5,
                "result": list_json
            }
        ]
    }
    return json.dumps(result, indent=4)

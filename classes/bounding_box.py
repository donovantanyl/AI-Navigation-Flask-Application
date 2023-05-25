class BoundingBox:
    def __init__(self, label, conf, xyxy):
        self.__label = label
        self.__conf = float(conf)
        self.__x1 = float(xyxy[0])  # x-min
        self.__y1 = float(xyxy[1])  # y-min
        self.__x2 = float(xyxy[2])  # x-max
        self.__y2 = float(xyxy[3])  # y-max

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


# Check if the number label is inside bus label
def inside(bus, number):
    center_x, center_y = (number.get_x1() + number.get_x2()) / 2, (number.get_y1() + number.get_y2()) / 2
    return bus.get_x1() <= center_x <= bus.get_x2() and bus.get_y1() <= center_y <= bus.get_y2()
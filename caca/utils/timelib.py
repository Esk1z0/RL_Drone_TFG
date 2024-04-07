import datetime

class TimeLib():

    @staticmethod
    def getTimeStr():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    @staticmethod
    def getTimeData():
        return datetime.datetime.now()

    @staticmethod
    def unformatTimeStr(time: str):
        return datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")

    @staticmethod
    def timeDiffStr(time1: str, time2: str):
        timeData1 = TimeLib.unformatTimeStr(time1)
        timeData2 = TimeLib.unformatTimeStr(time2)

        diff = timeData2 - timeData1
        return diff.microseconds / 1000

    @staticmethod
    def timeDiffData(time1: datetime.datetime, time2: datetime.datetime):
        diff = time2 - time1
        return diff.microseconds /1000
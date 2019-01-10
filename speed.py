from datetime import datetime, timedelta
from time import sleep


class SpeedChecker(object):
    start_time = ''
    end_time = ''
    dict_time = {}

    @classmethod
    def with_time_limit(cls, page, proxy, driver, server):
        try:
            proxy.new_har(page)
            driver.get(page)
            sleep(5)
            requests = proxy.har
            entries = requests['log']['entries']

            for each in entries:
                cls.dict_time[each['startedDateTime']] = each['time']

            for each in cls.dict_time.keys():

                if cls.start_time == '' or cls.start_time > datetime.fromisoformat(each):
                    cls.start_time = datetime.fromisoformat(each)

                milli = cls.dict_time[each]
                if cls.end_time == '' or cls.end_time < datetime.fromisoformat(each) + timedelta(milliseconds=milli):
                    cls.end_time = datetime.fromisoformat(each) + timedelta(milliseconds=milli)

            time_load = cls.end_time - cls.start_time
            server.stop()
            driver.quit()
            return str(time_load)

        except:
            proxy.close()
            driver.quit()
            return "Ошибочка. Проверь URL, должно начинаться с http:// or https://"

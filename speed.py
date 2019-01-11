from datetime import datetime, timedelta
from time import sleep


class SpeedChecker(object):

    def with_time_limit(self, page, proxy, driver, server):
        start_time = ''
        end_time = ''
        dict_time = {}
        try:
            proxy.new_har(page)
            driver.get(page)
            sleep(5)
            requests = proxy.har
            entries = requests['log']['entries']

            for each in entries:
                dict_time[each['startedDateTime']] = each['time']

            for each in dict_time.keys():

                if start_time == '' or start_time > datetime.fromisoformat(each):
                    start_time = datetime.fromisoformat(each)

                milli = dict_time[each]
                if end_time == '' or end_time < datetime.fromisoformat(each) + timedelta(milliseconds=milli):
                    end_time = datetime.fromisoformat(each) + timedelta(milliseconds=milli)

            time_load = end_time - start_time
            server.stop()
            driver.quit()
            return str(time_load)

        except:
            server.stop()
            driver.quit()
            return "Ошибочка. Проверь URL, должно начинаться с http:// or https://"

    def with_loadEventEnd(self, page, driver):
        try:
            driver.get(page)
            time = timedelta(milliseconds=driver.execute_script(
                "return ( window.performance.timing.loadEventEnd - window.performance.timing.navigationStart )"))

            return str(time)

        except:
            driver.quit()
            return "Ошибочка. Проверь URL, должно начинаться с http:// or https://"

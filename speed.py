from datetime import datetime, timedelta
from time import sleep


class SpeedChecker(object):

    def with_time_limit(self, page, proxy, driver, server, time=5):
        start_time = ''
        end_time = ''
        dict_time = {}
        try:
            proxy.new_har(page)
            driver.get(page)
            sleep(time)
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

        except:  # TODO add right exceptions
            server.stop()
            driver.quit()
            return "Error. Check URL. URL must start with http:// or https://"

    def with_loadEventEnd(self, page, driver):
        try:
            driver.get(page)
            time = timedelta(milliseconds=driver.execute_script(
                "return ( window.performance.timing.loadEventEnd - window.performance.timing.navigationStart )"))

            return str(time)

        except:  # TODO add right exceptions
            driver.quit()
            return "Error. Check URL. URL must start with http:// or https://"

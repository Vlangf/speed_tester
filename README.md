# Page opening speed tester
Now implemented are 2 methods of measuring the speed of opening a web page.  

####First method:
>With proxy. Wait for the end of all requests that are called when opening the page.  
We need install 'BrowserMob-Proxy' https://github.com/automatedtester/browsermob-proxy-py  

    Example:
    
    from speed import SpeedChecker
    from browsermobproxy import Server
    from selenium import webdriver
       
    def set_proxy_and_driver():
        server = Server("~/browsermob-proxy/bin/browsermob-proxy")
        server.start()
        proxy = server.create_proxy()

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
        driver = webdriver.Chrome(chrome_options=chrome_options)

        return server, proxy, driver


        def test_url_opening_speed():
        url = 'http://example.com'
        server, proxy, driver = set_proxy_and_driver()
        time_load = SpeedChecker().with_time_limit(url, proxy, driver, server)
        
        print(url, time)

####Second method:
>Wait browser method "loadEventEnd"

    Example:
    
    from speed import SpeedChecker
    from selenium import webdriver

    def set_driver():
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
        driver = webdriver.Chrome(chrome_options=chrome_options)

        return driver

    def test_url_opening_speed():
        url = 'http://example.com'

        driver = set_driver()
        time_load = SpeedChecker().with_loadEventEnd(url, driver)
        print(url, time)

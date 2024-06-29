from selenium import webdriver


class SingletonWebDriver:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonWebDriver, cls).__new__(cls, *args, **kwargs)
            cls._instance.init_driver()
        return cls._instance

    def init_driver(self):
        self.driver = webdriver.Chrome(keep_alive=True)

    def get_driver(self):
        return self.driver

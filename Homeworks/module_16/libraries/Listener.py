from robot.libraries.BuiltIn import BuiltIn


class Listener:
    ROBOT_LISTENER_API_VERSION = 2
    screenshot_tag: str

    def __get_screenshot_tag_name(self):
        vars = BuiltIn().get_variables()
        res = [item[1] for item in vars.items() if item[0] == "${SCREENSHOT_TAG}"]
        return res[0]

    def start_suite(self, data, result):
        self.screenshot_tag = self.__get_screenshot_tag_name()

    def end_keyword(self, name, attributes):
        if (self.screenshot_tag in attributes['tags']):
            selenium_lib = BuiltIn().get_library_instance('SeleniumLibrary')
            print(f'\nTook a screenshot after {name} keyword execution')
            selenium_lib.capture_page_screenshot()

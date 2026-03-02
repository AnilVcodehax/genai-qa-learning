import json
from core.action_handler import ActionHandler
from core.logger import get_logger


print("Keyword Engine Loaded---")
logger = get_logger("KeywordEngine")
class KeywordEngine:

    def __init__(self, driver):
        self.driver = driver
        self.action_handler = ActionHandler(driver)

    def execute_test_file(self, file_path):
        with open(file_path, "r") as file:
            test_cases = json.load(file)

        for test in test_cases:
            self.execute_test(test)

    def execute_test(self, test_data):
        test_name = test_data.get("test_name", "Unnamed Test")
        #print(f"\n===== Executing Test: {test_name} =====")
        logger.info(f"\n===== Executing Test: {test_name} =====")
        
        steps = test_data.get("steps", [])

        for step_number, step in enumerate(steps, start=1):
            action = step.get("action")
            locator = step.get("locator")
            value = step.get("value")

            #print(f"Step {step_number}: {action}")
            logger.info(f"Step {step_number}: {action}")

            if not hasattr(self.action_handler, action):
                raise Exception(f"Action '{action}' is not implemented in ActionHandler.")

            method = getattr(self.action_handler, action)

            try:
                # Execute the action
                if locator and value:
                    method(locator, value)
                elif locator:
                    method(locator)
                elif value:
                    method(value)
                else:
                    method()

            except AssertionError as ae:
                # Capture screenshot on assertion failure
                logger.error(f"Assertion failed on step {step_number}: {ae}")
                self.action_handler.take_screenshot(test_name=test_name, step_name=f"Step{step_number}_{action}")
                raise  # re-raise the assertion error
            
            except Exception as e:
                # Capture screenshot on assertion failure
                logger.error(f"Exception occurred on step {step_number}: {e}")
                self.action_handler.take_screenshot(test_name=test_name, step_name=f"Step{step_number}_{action}")
                raise  # re-raise the assertion error
            

        #print(f"===== Completed: {test_name} =====\n")
        logger.info(f"===== Logger Completed Test: {test_name} =====")
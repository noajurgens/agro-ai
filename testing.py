# Testing

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class PythonTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    def tearDown(self):
        self.driver.close()

    def test_all_healthy(self):
        self.driver.get('http://127.0.0.1:5001/')

        try_button = self.driver.find_element_by_name("try-button")
        try_button.click()

        while (self.driver.find_elements_by_id("choice-Healthy")):
            # print('finding elements')
            healthy_choice = self.driver.find_element_by_id("choice-Healthy")
            healthy_choice.click()
            submit_button = self.driver.find_element_by_id("submit-btn")
            submit_button.click()

        # print("out of while loop")
        confidence_val = self.driver.find_element_by_name("confidence-val")

        self.assertEqual("Confidence: 100.00%", confidence_val.text)

    def test_all_unhealthy(self):
        self.driver.get('http://127.0.0.1:5001/')

        try_button = self.driver.find_element_by_name("try-button")
        try_button.click()

        while (self.driver.find_elements_by_id("choice-Unhealthy")):
            # print('finding elements')
            healthy_choice = self.driver.find_element_by_id("choice-Unhealthy")
            healthy_choice.click()
            submit_button = self.driver.find_element_by_id("submit-btn")
            submit_button.click()

        # print("out of while loop")
        confidence_val = self.driver.find_element_by_name("confidence-val")

        self.assertEqual("Confidence: 100.00%", confidence_val.text)


    def test_retrain_with_new_data(self):
        self.driver.get('http://127.0.0.1:5001/')
        try_button = self.driver.find_element_by_name("try-button")
        try_button.click()

        while (self.driver.find_elements_by_id("choice-Healthy")):
                print('finding elements')
                healthy_choice = self.driver.find_element_by_id("choice-Healthy")
                healthy_choice.click()
                submit_button = self.driver.find_element_by_id("submit-btn")
                submit_button.click()
        
        confidence_val = self.driver.find_element_by_name("confidence-val")
        self.assertEqual("Confidence: 100.00%", confidence_val.text)

        checkboxes = self.driver.find_elements_by_xpath("//input[@name='healthy']")
        for checkbox in checkboxes[:10]:
            checkbox.click()
                
        retrain_button = self.driver.find_element_by_id("retrain-model-btn")
        retrain_button.click()

        time.sleep(6)
        confidence_val = self.driver.find_element_by_name("confidence-val-intermediate")

        self.assertNotEqual("Confidence: 100.00%", confidence_val.text)

    def test_retrain_no_new_data(self):
        self.driver.get('http://127.0.0.1:5001/')

        try_button = self.driver.find_element_by_name("try-button")
        try_button.click()

        while (self.driver.find_elements_by_id("choice-Healthy")):
                healthy_choice = self.driver.find_element_by_id("choice-Healthy")
                healthy_choice.click()
                submit_button = self.driver.find_element_by_id("submit-btn")
                submit_button.click()
        
        confidence_val = self.driver.find_element_by_name("confidence-val")
        self.assertEqual("Confidence: 100.00%", confidence_val.text)
                
        retrain_button = self.driver.find_element_by_id("retrain-model-btn")
        retrain_button.click()

        time.sleep(10)
        confidence_val = self.driver.find_element_by_name("confidence-val")

        self.assertEqual("Confidence: 100.00%", confidence_val.text)
    
    def test_find_ground_truth_healthy(self):
        self.driver.get('http://127.0.0.1:5001/')

        try_button = self.driver.find_element_by_name("try-button")
        try_button.click()

        while (self.driver.find_elements_by_id("choice-Healthy")):
                healthy_choice = self.driver.find_element_by_id("choice-Healthy")
                healthy_choice.click()
                submit_button = self.driver.find_element_by_id("submit-btn")
                submit_button.click()
        
        if (self.driver.find_elements_by_id("DSC05318.JPG")):
            diagnosis = self.driver.find_element_by_id("DSC05318.JPG-diagnosis")
            print(diagnosis.text)
            self.assertEqual("Professional Diagnosis: H", diagnosis.text)
    
    def test_find_ground_truth_unhealthy(self):
        self.driver.get('http://127.0.0.1:5001/')

        try_button = self.driver.find_element_by_name("try-button")
        try_button.click()

        while (self.driver.find_elements_by_id("choice-Healthy")):
                healthy_choice = self.driver.find_element_by_id("choice-Healthy")
                healthy_choice.click()
                submit_button = self.driver.find_element_by_id("submit-btn")
                submit_button.click()
        
        if (self.driver.find_elements_by_id("DSC00337.JPG")):
            diagnosis = self.driver.find_element_by_id("DSC00337.JPG-diagnosis")
            print(diagnosis.text)
            self.assertEqual("Professional Diagnosis: B", diagnosis.text)


if __name__ == "__main__":
    unittest.main()
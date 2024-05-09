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

    """
    Scenario: User labels every image as healthy

    Expected Result: Resulting confidence level is 100%
    """
    def test_all_healthy(self):
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

    """
    Scenario: User labels every image as unhealthy

    Expected Result: Resulting confidence level is 100%
    """
    def test_all_unhealthy(self):
        self.driver.get('http://127.0.0.1:5001/')

        try_button = self.driver.find_element_by_name("try-button")
        try_button.click()

        while (self.driver.find_elements_by_id("choice-Unhealthy")):
            healthy_choice = self.driver.find_element_by_id("choice-Unhealthy")
            healthy_choice.click()
            submit_button = self.driver.find_element_by_id("submit-btn")
            submit_button.click()

        confidence_val = self.driver.find_element_by_name("confidence-val")

        self.assertEqual("Confidence: 100.00%", confidence_val.text)

    """
    Scenario: User initially labels every image as healthy. They then select 10 checkboxes indicating disagreement with the model's prediction and retrain the model based on this new data.

    Expected Result: Confidence level decreases and is no longer 100%.
    """
    def test_retrain_with_new_data(self):
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

        checkboxes = self.driver.find_elements_by_xpath("//input[@name='healthy']")
        for checkbox in checkboxes[:10]:
            checkbox.click()
                
        retrain_button = self.driver.find_element_by_id("retrain-model-btn")
        retrain_button.click()

        time.sleep(6)
        confidence_val = self.driver.find_element_by_name("confidence-val-intermediate")

        self.assertNotEqual("Confidence: 100.00%", confidence_val.text)

    """
    Scenario: User initially labels every image as healthy. They then select the option to retrain model based off checkboxes without actually checking any checkboxes, essentially retraining the model with no new data.

    Expected Result: Confidence level does not change and remains at 100%.
    """
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
    
    """
    Scenario: User labels every image as unhealthy so the machine believes all leafs are unhealthy. User then checks the box to display cases where the experts disagreed with the machine.

    Expected Result: Border around image 'DSC00136.JPG', which is a healthy leaf, turns red.
    """
    def test_find_ground_truth_healthy_incorrect_checked(self):
        self.driver.get('http://127.0.0.1:5001/')

        try_button = self.driver.find_element_by_name("try-button")
        try_button.click()

        while (self.driver.find_elements_by_id("choice-Unhealthy")):
                healthy_choice = self.driver.find_element_by_id("choice-Unhealthy")
                healthy_choice.click()
                submit_button = self.driver.find_element_by_id("submit-btn")
                submit_button.click()
        
        show_checkbox = self.driver.find_element_by_id("UnhealthyDiagnosisSwitch")
        show_checkbox.click()

        time.sleep(5)
        
        if (self.driver.find_elements_by_id("DSC00136.JPG")):
            diagnosis = self.driver.find_element_by_id("DSC00136.JPG")
            parent = diagnosis.find_element_by_xpath("..")
            parentStyle = parent.get_attribute('style')
            self.assertEqual("border: 3px solid red;", parentStyle)
    
    """
    Scenario: User labels every image as unhealthy so the machine believes all leafs are unhealthy. User does not check the box to display disagreements between experts and the model.

    Expected Result: There is no border around image 'DSC00136.JPG', which is a healthy leaf.
    """
    def test_find_ground_truth_healthy_incorrect_not_checked(self):
        self.driver.get('http://127.0.0.1:5001/')

        try_button = self.driver.find_element_by_name("try-button")
        try_button.click()

        while (self.driver.find_elements_by_id("choice-Unhealthy")):
                healthy_choice = self.driver.find_element_by_id("choice-Unhealthy")
                healthy_choice.click()
                submit_button = self.driver.find_element_by_id("submit-btn")
                submit_button.click()
        
        if (self.driver.find_elements_by_id("DSC00136.JPG")):
            diagnosis = self.driver.find_element_by_id("DSC00136.JPG")
            parent = diagnosis.find_element_by_xpath("..")
            parentStyle = parent.get_attribute('style')
            self.assertEqual("", parentStyle)
    
    """
    Scenario: User labels every image as healthy so the machine believes all leafs are healthy. User then checks the box to display cases where the experts disagreed with the machine.

    Expected Result: There is no border around image 'DSC00136.JPG', which is a healthy leaf.
    """
    def test_find_ground_truth_healthy_correct(self):
        self.driver.get('http://127.0.0.1:5001/')

        try_button = self.driver.find_element_by_name("try-button")
        try_button.click()

        while (self.driver.find_elements_by_id("choice-Healthy")):
                healthy_choice = self.driver.find_element_by_id("choice-Healthy")
                healthy_choice.click()
                submit_button = self.driver.find_element_by_id("submit-btn")
                submit_button.click()
        
        show_checkbox = self.driver.find_element_by_id("HealthyDiagnosisSwitch")
        show_checkbox.click()
        
        if (self.driver.find_elements_by_id("DSC00136.JPG")):
            diagnosis = self.driver.find_element_by_id("DSC00136.JPG")
            parent = diagnosis.find_element_by_xpath("..")
            parentStyle = parent.get_attribute('style')
            self.assertEqual("", parentStyle)
    
    """
    Scenario: User labels every image as healthy so the machine believes all leafs are healthy. User then checks the box to display cases where the experts disagreed with the machine.

    Expected Result: Border around image 'DSC00337.JPG', which is an unhealthy leaf, turns red.
    """
    def test_find_ground_truth_unhealthy_incorrect_checked(self):
        self.driver.get('http://127.0.0.1:5001/')

        try_button = self.driver.find_element_by_name("try-button")
        try_button.click()

        while (self.driver.find_elements_by_id("choice-Healthy")):
                healthy_choice = self.driver.find_element_by_id("choice-Healthy")
                healthy_choice.click()
                submit_button = self.driver.find_element_by_id("submit-btn")
                submit_button.click()
        
        show_checkbox = self.driver.find_element_by_id("HealthyDiagnosisSwitch")
        show_checkbox.click()

        time.sleep(5)
        
        if (self.driver.find_elements_by_id("DSC00337.JPG")):
            diagnosis = self.driver.find_element_by_id("DSC00337.JPG")
            parent = diagnosis.find_element_by_xpath("..")
            parentStyle = parent.get_attribute('style')
            self.assertEqual("border: 3px solid red;", parentStyle)
    
    """
    Scenario: User labels every image as healthy so the machine believes all leafs are healthy. User does not check the box to display cases where the experts disagreed with the machine.

    Expected Result: There is no border around image 'DSC00337.JPG', which is an unhealthy leaf.
    """
    def test_find_ground_truth_unhealthy_incorrect_not_checked(self):
        self.driver.get('http://127.0.0.1:5001/')

        try_button = self.driver.find_element_by_name("try-button")
        try_button.click()

        while (self.driver.find_elements_by_id("choice-Healthy")):
                healthy_choice = self.driver.find_element_by_id("choice-Healthy")
                healthy_choice.click()
                submit_button = self.driver.find_element_by_id("submit-btn")
                submit_button.click()
        
        if (self.driver.find_elements_by_id("DSC00337.JPG")):
            diagnosis = self.driver.find_element_by_id("DSC00337.JPG")
            parent = diagnosis.find_element_by_xpath("..")
            parentStyle = parent.get_attribute('style')
            self.assertEqual("", parentStyle)
    
    """
    Scenario: User labels every image as unhealthy so the machine believes all leafs are unhealthy. User then checks the box to display cases where the experts disagreed with the machine.

    Expected Result: There is no border around image 'DSC00337.JPG', which is an unhealthy leaf.
    """
    def test_find_ground_truth_unhealthy_correct(self):
        self.driver.get('http://127.0.0.1:5001/')

        try_button = self.driver.find_element_by_name("try-button")
        try_button.click()

        while (self.driver.find_elements_by_id("choice-Unhealthy")):
                healthy_choice = self.driver.find_element_by_id("choice-Unhealthy")
                healthy_choice.click()
                submit_button = self.driver.find_element_by_id("submit-btn")
                submit_button.click()
        
        show_checkbox = self.driver.find_element_by_id("UnhealthyDiagnosisSwitch")
        show_checkbox.click()
        
        if (self.driver.find_elements_by_id("DSC00337.JPG")):
            diagnosis = self.driver.find_element_by_id("DSC00337.JPG")
            parent = diagnosis.find_element_by_xpath("..")
            parentStyle = parent.get_attribute('style')
            self.assertEqual("", parentStyle)
    
    """
    Scenario: User gets to the final screen and checks the box to display cases where the expert disagreed with the model. User then clicks on an image that experts marked as unhealthy.

    Expected Result: A modal with the version of the images with boxes is displayed.
    """
    def test_find_boxed_image(self):
        self.driver.get('http://127.0.0.1:5001/')

        try_button = self.driver.find_element_by_name("try-button")
        try_button.click()

        while (self.driver.find_elements_by_id("choice-Healthy")):
                healthy_choice = self.driver.find_element_by_id("choice-Healthy")
                healthy_choice.click()
                submit_button = self.driver.find_element_by_id("submit-btn")
                submit_button.click()
        
        show_checkbox = self.driver.find_element_by_id("HealthyDiagnosisSwitch")
        show_checkbox.click()
        
        if (self.driver.find_elements_by_id("DSC00307.JPG")):
            diagnosis = self.driver.find_element_by_id("DSC00307.JPG")
            diagnosis.click()
            time.sleep(5)
            modal_image = self.driver.find_elements_by_name("DSC00307.JPG-boxed")
            self.assertEqual(1, len(modal_image))
    
    """
    Scenario: User gets to the final screen and checks the box to display cases where the expert disagreed with the model. User then clicks on an image that experts marked as unhealthy.

    Expected Result: A modal with the normal version of the image (without boxes) is displayed.
    """
    def test_find_normal_image(self):
        self.driver.get('http://127.0.0.1:5001/')

        try_button = self.driver.find_element_by_name("try-button")
        try_button.click()

        while (self.driver.find_elements_by_id("choice-Healthy")):
                healthy_choice = self.driver.find_element_by_id("choice-Healthy")
                healthy_choice.click()
                submit_button = self.driver.find_element_by_id("submit-btn")
                submit_button.click()
        
        if (self.driver.find_elements_by_id("DSC00307.JPG")):
            diagnosis = self.driver.find_element_by_id("DSC00307.JPG")
            diagnosis.click()
            time.sleep(5)
            modal_image = self.driver.find_elements_by_name("DSC00307.JPG-normal")
            self.assertEqual(1, len(modal_image))

if __name__ == "__main__":
    unittest.main()
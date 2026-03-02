import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

print("Anil informing that --Script Started")

with open("testcases.json") as f:
    data = json.load(f)

#print("JSON Loaded:", data)

options = Options()
driver = webdriver.Chrome(options=options)
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")
report_data = []
pass_count = 0
fail_count = 0
for test in data["test_cases"]:
    print("\n-----------------------------------")
    print(f"Running Scenario: {test['scenario']}")
    
    driver.get(test["url"])
    #time.sleep(10)
    wait = WebDriverWait(driver,15)
   
    # Click "Form Authentication"
    #link = driver.find_element(By.LINK_TEXT, "Form Authentication")
    #link.click()
    #time.sleep(10)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT,"Form Authentication"))).click()

    # Enter Username
    #driver.find_element(By.ID, "username").clear()
    #driver.find_element(By.ID, "username").send_keys(test['username'])
    
    # Enter Username
    wait.until(EC.visibility_of_element_located((By.ID,"username"))).clear()
    wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(test['username'])

    # Enter Password
    #driver.find_element(By.ID, "password").clear()
    #driver.find_element(By.ID, "password").send_keys(test["password"])

    # Enter Password
    wait.until(EC.visibility_of_element_located((By.ID,"password"))).clear()
    wait.until(EC.visibility_of_element_located((By.ID,"password"))).send_keys(test["password"])

    # Click Login button
    #driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    #time.sleep(10)

    # Click Login button
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()


    
    # Assertion (Validation)
    # message = driver.find_element(By.ID, "flash").text
    # time.sleep(10)
    
    # Assertion (Validation)
    message = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text

    status = ""
    screenshot_name = ""
    if test["expected_message"] in message:
        print("✅ Test Passed")
        pass_count += 1
        status = "Passed"
    else:
        print("❌ Test Failed")
        fail_count += 1
        status = "Failed"

        screenshot_name = f"screenshots/{test['scenario'].replace(' ', '_')}.png"
        driver.save_screenshot(screenshot_name)
        print(f"📸 Screenshot saved: {screenshot_name}")

report_data.append({
    "scenario": test["scenario"],
    "status": status,
    "screenshot": screenshot_name
})
print("\n========== TEST SUMMARY ==========")

html_content = """
<html>
<head>
    <title>Automation Test Report</title>
</head>
<body>
    <h1>Test Execution Report</h1>
    <h2>Summary</h2>
    <p>Total Passed: {}</p>
    <p>Total Failed: {}</p>
    <hr>
    <h2>Detailed Results</h2>
    <table border="1" cellpadding="5" cellspacing="0">
        <tr>
            <th>Scenario</th>
            <th>Status</th>
            <th>Screenshot</th>
        </tr>
""".format(pass_count, fail_count)

for result in report_data:
    screenshot_link = (
        f"<a href='{result['screenshot']}'>View</a>"
        if result["screenshot"] else "N/A"
    )

    html_content += f"""
        <tr>
            <td>{result['scenario']}</td>
            <td>{result['status']}</td>
            <td>{screenshot_link}</td>
        </tr>
    """

html_content += """
    </table>
</body>
</html>
"""

with open("report.html", "w") as f:
    f.write(html_content)

print("📄 HTML Report Generated: report.html")

print(f"Total Passed: {pass_count}")
print(f"Total Failed: {fail_count}")

input("Press Enter to close browser...")
driver.quit()
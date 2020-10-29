#!/usr/bin/env python3
import requests
import sys
import os

url_main = "http://localhost:8090/api/"
url_status = "main/status"
url_screenshot = 'stelaction/do'
url_time = "main/time"
no_of_observations = 7310

for observation in range(no_of_observations):
    # Get the status of stellarium
    status_response = requests.get(url_main + url_status)
    if status_response.status_code != 200:
        raise Exception("Bad get response: " + str(status_response.status_code))
    # Get the time of the observation
    time = status_response.json().get('time')
    if not time:
        raise Exception("Invalid time")
    # Create a screenshot of the current view
    screenshot_response = requests.post(url_main + url_screenshot, data={'id': 'actionSave_Screenshot_Global'})
    if screenshot_response.status_code != 200:
        raise Exception("Bad screenshot response: " + str(screenshot_response.status_code))
    screenshotName = sys.path[0] + '/' + 'stellarium-000.png'
    # Downsize the image
    os.system('sips -Z 300 ' + screenshotName)
    # Rename the image file
    local_time = time.get('local')
    newName = sys.path[0] + '/' + local_time[:13] + local_time[14:16] + '.png'
    os.rename(screenshotName, newName)

    # Increment the observation time by 12 hours
    new_time = time.get('jday') + 0.5
    set_response = requests.post(url_main + url_time, data={'time': str(new_time)})
    if set_response.status_code != 200:
        raise Exception("Bad set response: " + str(set_response.status_code))
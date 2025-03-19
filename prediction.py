
import os
from inference_sdk import InferenceHTTPClient
import threading
import time
# Initialize the inference client
client = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="*****************************"
)
#API Key about Notifications
api_key = "********************"  # Replace with your actual API key
#-----------------------------------------------------------

def noti(text):
    from pushbullet import Pushbullet
    pb = Pushbullet(api_key)
    push = pb.push_note("Stock Alert", text)
    print("Notification sent!")
#---------------------------------------------------------------
def loki(alerts):
            print(alerts)
            noti(alerts[0])
            alerts.clear()

#----------------------------------------------------------
def mpredict(filepath):
    # Run inference
    result = client.run_workflow(
        workspace_name="YOUR_WORKSPACE_NAME_HERE",
        workflow_id="YOUR_WORKFLOW_ID_HERE",
        images={"image": filepath},
        use_cache=True
    )
    #print("result",result)

    # Process inference results
    m_threshold = 4  # Example threshold for 'm'
    s_threshold = 3 # Example threshold for 's'
    alerts = []

    for item in result:
        for prediction in item.get('predictions', {}).get('predictions', []):
            class_str = prediction['class']
            print(class_str)
            prefix = class_str[0]
            number_str = class_str[1:]

            try:
                number = int(number_str)
                if prefix == 'm' and number < m_threshold:
                    alerts.append("Stock below alert for matchbox")
                    loki(alerts)
                elif prefix == 's' and number < s_threshold:
                    alerts.append("Stock below alert for soapbox")
                    loki(alerts)
                
            except ValueError:
                alerts.append(f"Could not convert '{number_str}' to an integer: {number_str}")

#-------------------------------------------------------------------------------------------------------
def schedule_mpredict(filepath):
    for i in range(30):
        mpredict(filepath)
        [print("Prediction Ran Once------")]

        time.sleep(10)
    
    

if __name__ == '__main__':
    filepath = "O:\\WORK\\B.tech\\S6\\MiniProject\\Working\\uploads\\image.jpg"
    schedule_mpredict(filepath)

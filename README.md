# is-my-websitedown-alert
This is a short cron job python script that alerts when your chosen web page is down into discord slack or anywhere else with similar webhooks.

#run - pip install requests
#can be run as cron job in linux or Task Scheduler in Windows
#to add cron job do    crontab -e and the code bellow with your the alert.py directory, add it  to the bottonm of the cron file 
# */10 * * * * /usr/bin/python3 /path/to/your/folder/alert.py >> /path/to/your/folder/alert_log.txt 2>&1
# set for 10 min change the 10 to change this , use reccomended option 

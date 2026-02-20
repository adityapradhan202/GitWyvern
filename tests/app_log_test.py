# Testing application logs here
from utils import GeneralUtils

func_type = input("Enter function type, log or clear: ")

if func_type == "log":
    log_type = input("Enter log type: ")
    giturl = input("Enter Git URL: ")
    stamp = GeneralUtils.datetime_stamp()
    GeneralUtils.app_log(datetime_stamp=stamp, log_type=log_type, giturl=giturl)
elif func_type == "clear":
    GeneralUtils.clear_app_log()

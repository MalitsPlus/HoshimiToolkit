import sys
import requests
import rich_console as console
from os import _exit as exit
from requests.exceptions import SSLError, ProxyError

_MAX_RETRIES = 5

def send_request(func, url, data=None, headers=None, verify=True, retries=0) -> requests.Response:
    if retries >= _MAX_RETRIES:
        console.error(f"Get {url} failed. Stopping process.")
        exit(-1)
    try:
        response = func(url, data=data, headers=headers, verify=verify)
        if response.status_code != 200:
            raise f"Abnormal status code {response.status_code}."
    # except SSLError:
    #     console.error("An SSLError has occured, please check your network settings.")
    #     console.error("Stopping process.")
    #     exit(-1)
    # except ProxyError:
    #     console.error("An ProxyError has occured, please check your network settings.")
    #     console.error("Stopping process.")
    #     exit(-1)
    except:
        console.error(f"An error occurred during send request to {url}.")
        console.error(f"ErrInfo: {sys.exc_info()[0]}.")
        console.error(f"Retries({retries + 1}/{_MAX_RETRIES}).")
        response = send_request(func, url, data, headers, verify, retries + 1)
    return response


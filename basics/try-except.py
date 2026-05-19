import requests
import json

try:
    res = requests.get("https://wttr.in?format=j1", timeout=5)
    res.raise_for_status()

    print(res.status_code)
    # print(res.text)
    data = res.json()
    print(data["current_condition"][0]["FeelsLikeC"])

except requests.exceptions.ConnectionError as e:
    print("Connection Failed. Please Try Again.")

except requests.exceptions.RequestException as e:
    print("Request failed: ", e)

except Exception as e:
    print("Something went wrong...", e)

finally:
    pass

# File Exception
# try:
#     with open("test.txt", "r") as f:
#         c = f.read()
#         print(c)
# except FileNotFoundError as e:
#     print("File not found.", e)
# except Exception as e:
#     print(e)

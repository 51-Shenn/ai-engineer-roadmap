import requests
import os
import json

def start():
    my_wtr_link = "https://wttr.in/Malaysia?format=j1"
    file_path = "files/wttr.json"

    try:
        print("Connecting to weather api...")
        res = requests.get(my_wtr_link, timeout=2)
        res.raise_for_status()

        # print(res.text) # can use f.write() directly

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(res.json(), f, indent=2)

        if res.status_code == 200:
            print("Successfully connected!")
        else:
            print("Connection unsuccessful.")
            return

    except Exception as e:
        print(e)
        print("Connection failed, please try again.")

def main():
    os.system("clear")
    start()

    regions = ["johor", "kedah", "kelantan", "melaka", "negeri-sembilan", "pahang", "perak", "perlis", "penang", "sabah", "sarawak", "selangor", "terengganu", "kuala-lumpur", "putrajaya", "labuan"]

    for i, r in enumerate(regions):
        if "-" in r:
            r1, r2 = r.split("-")
            region_full = f"{r1.capitalize()} {r2.capitalize()}"
            print(f"Region {i + 1}: {region_full}")
        else:
            print(f"Region {i + 1}: {r.capitalize()}")

    print()

    while True:
        choice = int(input("Choose a region to check its weather: "))

        if choice < 1 or choice > len(regions):
            print(f"Invalid choice. Please enter range between 1 - {len(regions)}")
            break

        chosen_region = f"https://wttr.in/{regions[choice - 1]}?format=j1"

        try:
            res = requests.get(chosen_region, timeout=5)
            res.raise_for_status()

            data = res.json()

            with open("files/chosen.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            current_condition = data["current_condition"]
            selected_region = regions[choice - 1]
            display_region = selected_region.replace("-", " ").title()

            temp = [current_condition[0]["temp_C"], current_condition[0]["temp_F"]]

            print(f"{display_region} (Celsius): {temp[0]} ℃")
            print(f"{display_region} (Fahrenheit): {temp[1]} ℉")

        except Exception as e:
            print("Something went wrong...")
            print(e)

if __name__ == "__main__":
    main()

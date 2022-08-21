import requests
import threading
import urllib3
import time
from datetime import datetime

urllib3.disable_warnings()


def main() -> None:
    # startTime = datetime.now()
    result_status: list = []
    result: dict = {}

    def start_reqs(i: str, url: str, api: str) -> None:
        proxy_host = "proxy.crawlera.com:8011"
        headers = {}

        response = requests.get(
            url,
            proxies={
                "http": f"http://{api}:@{proxy_host}/",
                "https": f"http://{api}:@{proxy_host}/",
            },
            verify=False, headers=headers
        )

        name = i + ".html"
        with open(name, "w") as f:
            f.write(response.text)
            f.close()

        debug_data: str = """
        	=====================================================================
        	Request No [{}]
        	=====================================================================
        	Requesting [{}]
        	through proxy [{}]

        	Request Headers:
        	{}

        	Response Time: {}
        	Response Code: {}
        	Response Headers:
        	{}
        	Response Text:
        	{}
        	""".format(
            i,
            url,
            proxy_host,
            response.request.headers,
            response.elapsed.total_seconds(),
            response.status_code,
            response.headers,
            response.text,
        )
        print(f"Request No {str(i)} retunred {response.status_code}")
        name = i + ".html"
        open(name, "wb").write(response.content)

        with open("output.txt", "a", encoding="utf-8") as outfile:
            outfile.write(debug_data)

        if response.status_code == 200:
            result_status.append(response.status_code)
        else:
            result_status.append(response.status_code)

    reqs = input("How many requests? ")

    reqs = int(reqs)
    url = input("Enter the url? ")
    api = input("Enter the API key? ")
    threads: list = []

    for i in range(reqs):
        thread = threading.Thread(target=start_reqs, args=(str(i), url, api))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    for code in result_status:
        no_of_status = result_status.count(code)
        result[code] = no_of_status
    print(result)
    # print(datetime.now() - startTime)


if __name__ == "__main__":
    main()

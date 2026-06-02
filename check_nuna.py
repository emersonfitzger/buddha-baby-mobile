#!/usr/bin/env python3
import os, re, sys, requests

URL = "https://nunababy.com/usa/triv-lx-pipa-urbn-travel-system"
NTFY_TOPIC = os.environ["NTFY_TOPIC"]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def main():
    try:
        r = requests.get(URL, headers=HEADERS, timeout=30)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Skipping this check - Nuna site issue: {e}")
        return

    html = r.text.lower()
    meta = re.search(r'product:availability"\s+content="([^"]+)"', html)
    availability = meta.group(1) if meta else None
    out_of_stock = availability == "out of stock" or ">out of stock<" in html

    if out_of_stock:
        print("Still out of stock.")
        return

    requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=f"Nuna TRIV lx + PIPA urbn is BACK IN STOCK\n{URL}",
        headers={
            "Title": "Nuna travel system - in stock!",
            "Priority": "urgent",
            "Tags": "rotating_light,baby_symbol",
            "Click": URL,
        },
        timeout=15,
    )
    print("In stock - notification sent.")

if __name__ == "__main__":
    main()


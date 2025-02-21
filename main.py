import requests 


API_KEY = 'ca860e196ad7aa82316d044c30dc898cce252d1579ed53ca93c4861312fe306b'


def check_url(url):
    api_url = "https://www.virustotal.com/api/v3/urls"

    data = {'url':url}

    headers = {
        'x-apikey':API_KEY
    }

    respons = requests.post(api_url,data=data,headers=headers)

    if respons.status_code == 200:
        analysis_id=respons.json()['data']['id']
        report_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
        report_request = requests.get(report_url,headers=headers)
        report_data = report_request.json()

        stats = report_data['data']['attributes']['stats']
        malicious = stats["malicious"]
        suspicious = stats["suspicious"]
        harmless = stats["harmless"]      

        if malicious > 0:
            print("🚨 this url is not safe ")
        else:
            print("✅ the url is safe")
    
    else:
        print("❌ فشل في الاتصال بـ VirusTotal!")

url = input("enter url:")

check_url(url)

import requests, json

class IPTracker:
    api_key = '18e2fa5c30e08d4310ef5cdb1e27b8bb'
    url = 'http://api.ipstack.com/{ip}?access_key={key}'

    def check_ip(self, request_data=None):
        
        client_ip = request_data.META.get('REMOTE_ADDR')
        data = {
            'ip': client_ip,
            'key': self.api_key
        }
        r = requests.get(self.url.format(**data))
        return json.loads(r.text)

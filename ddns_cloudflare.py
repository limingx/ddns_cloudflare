#!/usr/bin/python3
# -*- coding:utf-8 -*-

import requests
import json
import re

def get_ip(url):
    try:
        resp = requests.get(url).text.strip()

        pattern=r'\d{,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        ip=re.search(pattern, resp)
        if not ip:
            raise NameError('Not found public ip.')
        return ip[0]
    except Exception as e:
        print('get ip failed, error :\n{}'.format(e))
        sys.exit(1)
    return 0

def get_record_id(dns_name, zone_id, token):
    resp = requests.get(
            'https://api.cloudflare.com/client/v4/zones/{}/dns_records'.format(zone_id),
            headers={
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
                }
            ).json()
    if not resp['success']:
        print('get dns record id failed.')
        sys.exit(1)
 
    domains = resp['result']
    for domain in domains:
        if dns_name == domain['name']:
            return domain['id']
    return 0

def update_dns_record(dns_name, zone_id, token, dns_id, ip, proxied=False):
    resp = requests.put(
            'https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(zone_id, dns_id),
            json={
                'type': 'A',
                'name': dns_name,
                'content': ip,
                'proxied': proxied
                },
            headers={
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
                }
            ).json()
    if not resp['success']:
        print('update dns record failed.')
        sys.exit(1)

    return True

def dns_record_details(zone_id, dns_id, token):
    resp = requests.get(
            'https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(zone_id, dns_id),
            headers={
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            }
        ).json()

    return resp

def main():
    public_ip_query = 'https://ifconfig.me/ip'
    ddns_domain = 'sub.your-domain.com'
    dns_zone_id = 'your-dns-zone-id'
    dns_zone_token = 'your-dns-zone-token'

    dns_record_id = get_record_id(ddns_domain, dns_zone_id, dns_zone_token)
    dns_json = dns_record_details(dns_zone_id, dns_record_id, dns_zone_token)

    print('\nDDNS domain: {}'.format(ddns_domain))
    print('\nDns records :')
    print(json.dumps(dns_json, indent=2))
   
    ddns_domain_ip = dns_json['result']['content']
    public_ip = get_ip(public_ip_query)
    print('\nCurrent public ip : {} (via - {})'.format(public_ip, public_ip_query))

    if ddns_domain_ip == public_ip:
        print('\nNo changes to update.')
    else:
        print('\nUpdate dns records now...')
        print('{} -> {}'.format(ddns_domain_ip, public_ip))
        proxied=False
        result = update_dns_record(ddns_domain, dns_zone_id, dns_zone_token, dns_record_id, public_ip, proxied)
        if result:
            dns_json = dns_record_details(dns_zone_id, dns_record_id, dns_zone_token)
            print('\nNew records :')
            print(json.dumps(dns_json, indent=2))
            print('\nDns set succeed, this may take a few minutes to take effect.')

    return 0

main()

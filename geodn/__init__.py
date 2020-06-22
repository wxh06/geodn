from telnetlib import Telnet
import sys

import requests


def main(domain, provider=None):
    ipa = resolve(domain, provider)
    telnet = whois(ipa, 'apnic')  # TODO
    country = read_country(telnet)
    telnet.close()
    return country


def read_country(telnet):
    return telnet.expect([br'country: +([A-Z]{2})'])[1].group(1).decode()


def whois(ipa, source='apnic'):
    telnet = Telnet(f'whois.{source}.net', 43)
    telnet.write(bytes(ipa, encoding='utf-8') + b'\r\n')
    return telnet


def resolve(domain_name, provider=None):
    for answer in doh({'name': domain_name}, provider)['Answer']:
        if answer['type'] == 1:
            return answer['data']
    for answer in doh({'name': domain_name}, provider)['Answer']:
        if answer['type'] == 5:
            return resolve(answer['data'], provider)
    raise Exception


def doh(params, provider=None):
    provider = provider or cloudflare
    try:
        res = provider(params)
    except TypeError:
        res = {
            'ali': ali, 'cloudflare': cloudflare, 'google': google
        }[provider.strip().lower()](params)
    res.raise_for_status()
    return res.json()


def ali(params):
    return requests.get('https://dns.alidns.com/resolve', params=params)


def cloudflare(params):
    return requests.get(
        'https://cloudflare-dns.com/dns-query',
        params=params,
        headers={'accept': 'application/dns-json'}
    )


def google(params):
    return requests.get('https://dns.google/resolve', params=params)


if __name__ == '__main__':
    print(main(sys.argv[1], sys.argv[2]))

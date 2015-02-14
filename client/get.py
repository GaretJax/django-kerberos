#!/usr/bin/env python

import click
import requests
import kerberos


URL = 'http://kerbtest.dev/'


def do(s, *args, **kwargs):
    click.secho(' => ' + s.format(*args, **kwargs), fg='yellow')


def done(s, *args, **kwargs):
    click.secho('<=  ' + s.format(*args, **kwargs), fg='green')


def www_auth(response):
    auth_fields = {}
    for field in response.headers.get("www-authenticate", "").split(","):
        kind, __, details = field.strip().partition(" ")
        auth_fields[kind.lower()] = details.strip()
    return auth_fields


@click.command()
def get_page(url=URL):
    do('Requesting {}', url)
    r = requests.get(url)
    done('{} - WWW-AUTHENTICATE: {}',
         r.status_code, r.headers["www-authenticate"])

    auth = www_auth(r)
    assert 'negotiate' in auth

    do('Checking kerberos credentials')
    assert kerberos.checkPassword(
        'admin/admin',
        'test',
        'HTTP/kerbtest',
        'DJKERB.DEV',
    )
    done('Credentials ok')

    # addprinc HTTP/kerbtest

    do('Getting kerberos ticket')
    __, krb_context = kerberos.authGSSClientInit(
        'HTTP@kerbtest',
    )
    kerberos.authGSSClientStep(krb_context, '')
    negotiate_details = kerberos.authGSSClientResponse(krb_context)
    done('Negotiate details: {}', negotiate_details)

    do('Requesting {} with auth', url)
    headers = {'Authorization': 'Negotiate ' + negotiate_details}
    r = requests.get(url, headers=headers)
    done('Status code: {}', r.status_code)


if __name__ == '__main__':
    get_page()

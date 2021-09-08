#!/usr/bin/python3

from pyzabbix import ZabbixAPI
import logging
import config
import optparse

if config.LOGGING:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')


def get_service_list(host, username, password):
    services_list = ''
    zapi = ZabbixAPI(config.HOST)
    logging.info('Connecting to the server')
    zapi.login(config.USER_NAME, config.PASSWORD)
    logging.info('Requesting service-list')
    services = zapi.service.get()
    for service in services:
        services_list += service['serviceid'] + ' ' + service['name'] + '\n'
    return services_list


def get_service_state(host, username, password, service_id):
    zapi = ZabbixAPI(config.HOST)
    logging.info('Connecting to the server')
    zapi.login(config.USER_NAME, config.PASSWORD)
    logging.info('Requesting service-status')
    service = zapi.service.get(serviceids=service_id)
    if len(service) == 0:
        return 'Error!'
    else:
        return service[0]['status']


if __name__ == '__main__':
    logging.info('Script start')
    p = optparse.OptionParser()
    p.add_option('--list', '-l', action='store_true', help='show IDs of the services')
    p.add_option('--id', '-i', help='get service state by id')
    options, arguments = p.parse_args()
    if options.list:
        services_list = get_service_list(config.HOST, config.USER_NAME, config.PASSWORD)
        print(services_list)
    elif options.id:
        print(get_service_state(config.HOST, config.USER_NAME, config.PASSWORD, options.id))
    else:
        p.print_help()

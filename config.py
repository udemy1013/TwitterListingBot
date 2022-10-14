import configparser

config = configparser.ConfigParser()

config['BASE'] = {
    'user_id': 'k10002hash',
    'password': 'yasashiku1',
    'target_id': 'oliverlesterr',
    'listing_num': 1500

}
with open('/config.ini', 'w') as file:
    config.write(file)

print("Hello")
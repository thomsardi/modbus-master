from main import main
import json


def sending_all_config(data: list, is_update: int):
    # open json config file
    # config_file = json.load(open('modbus_config.json'))
    config_file = json.load(open('modbus_config_test.json'))
    config = config_file['config']

    # update config all slave
    print("Updating parameter...")
    for cfg in config :
        id = cfg['slave_id']
        param = cfg['param']
        # clear list
        param.clear()
        # add new data
        for d in data:
            param.append(d)
    
    # update dict
    config_file['config'] = config
    config_file['update'] = is_update
    
    # write to file
    with open('modbus_config_test.json', 'w') as outfile:
        json.dump(config_file, outfile)


def sending_slave_config(data: list, is_update: int, id_slave: int):
    config_file = json.load(open('modbus_config_test.json'))
    config = config_file['config']

    # update config id slave
    print("Updating parameter...")
    for cfg in config :
        id = cfg['slave_id']
        param = cfg['param']
        if id == id_slave:
            # clear list
            param.clear()
            # add new data
            for d in data:
                param.append(d)
            
    # update dict
    config_file['config'] = config
    config_file['update'] = is_update

    # write to file
    with open('modbus_config_test.json', 'w') as outfile:
        json.dump(config_file, outfile)
    
    main()


datas = [
    { "name" : "charging_voltage_limit", "value" : 155 }
]
is_update = 1
id_slave = 172

# sending_all_config(datas, is_update)
sending_slave_config(datas, is_update, id_slave)

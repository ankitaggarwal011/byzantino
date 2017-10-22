from config import ClientConfig
from config import ReplicaConfig


def parse_config_file(filename):
    config = {}
    with open(filename, 'r') as f:
        for line in f:
            if line[0] == '#':
                continue
            (key, sep, val) = line.partition('=')
            # if the line does not contain '=', it is invalid and hence ignored
            if len(sep) != 0:
                val = val.strip()
                #config[key.strip()] = int(val) if str.isdecimal(val) else val
                config[key.strip()] = val

    return config


if __name__ == '__main__':
    config = parse_config_file("./config/c1.txt")
    client_config = ClientConfig(config)
    replica_config = ReplicaConfig(config)
    print(client_config.__str__())
    print('Replica config: ' + replica_config.__str__())

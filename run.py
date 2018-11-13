import os
import sys
import toml
from multiprocessing import Process

def main():
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.toml"
    try:
        config = toml.load(config_path)
    except:
        return
    global_config = config.get('global', {})
    server_config = config.get('server', {})
    worker_config = config.get('worker', {})
    test_config = config.get('test', {})
    address = global_config.get('address', "127.0.0.1")
    port = global_config.get('port', 3333)
    print(f"URL: http://{address}:{port}/")
    if server_config.get('enable'):
        print("Server: ON")
        import server
        Process(target=server.main, args=("0.0.0.0", port)).start()
    else:
        print("Server: OFF")
    if worker_config.get('enable'):
        print("Worker: ON")
        import worker
        Process(target=worker.main, args=(address, port, worker_config.get('headless', False), worker_config.get('workers', 2), worker_config.get('delay', 2))).start()
    else:
        print("Worker: OFF")
    if test_config.get('enable'):
        print("Test: ON")
        import test
        for _ in range(test_config.get('thread', 2)):
            Process(target=test.main, args=(address, port)).start()
    else:
        print("Test: OFF")

if __name__ == "__main__":
    main()

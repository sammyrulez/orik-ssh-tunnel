from sshtunnel import SSHTunnelForwarder
import logging


def stop_tunnel(server):
    server.stop()


def start_tunnel(conf, forward):
    server = SSHTunnelForwarder(
        conf.host_name,
        ssh_username=conf.user,
        remote_bind_address=(
            forward.host, int(forward.local_port)),
        local_bind_address=(
            "0.0.0.0", int(forward.remote_port)),
        # ssh_password="xyz"
    )
    server.start()
    logging.info(" Server started %s", conf.host_name)
    return server

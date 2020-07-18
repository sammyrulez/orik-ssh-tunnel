
def bastion():
    print("starting")
    with sshtunnel.open_tunnel(
        ('52.213.9.19', 22),
        ssh_username="samuele.reghenzi",
        ssh_private_key_password="bazinga",
        remote_bind_address=('10.139.12.178', 22),
        local_bind_address=('0.0.0.0', 10022)
    ) as tunnel:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("connecting")
        client.connect('localhost', 10022)
        # do some operations with client session
        print("connected")
        client.close()

    print('FINISH!')


if __name__ == "__main__":
    import paramiko
    import sshtunnel
    import time

    # bastion()

    from sshtunnel import SSHTunnelForwarder

    server = SSHTunnelForwarder(
        '52.213.9.19',
        ssh_username="samuele.reghenzi",
        ssh_private_key_password="bazinga",
        remote_bind_address=('10.139.12.178', 8080)
    )

    server.start()

    print(server.local_bind_port)  # show assigned local port
    # work with `SECRET SERVICE` through `server.local_bind_port`.
    time.sleep(60)
    server.stop()

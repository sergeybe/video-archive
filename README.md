# Video Archive

1. Create Python virtual environment and install developers packages:

```shell
mkvirtualenv video-archive -p `which python3`
pip install -r requirements-dev.txt
```

2. Run command for starting Vagrant virtual host:

```shell
vagrant up
```

3. Run command for provision of Vagrant virtaul host:

```shell
vagrant provision
```

4. Open url http://127.0.0.1:8080/ by browser.

Nice!

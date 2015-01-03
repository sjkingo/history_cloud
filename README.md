## history_cloud

Creates a pretty "tag" cloud of your bash history.

It requires the excellent [Jinja2 library](https://pypi.python.org/pypi/Jinja2).

### How to use

```
$ virtualenv history_cloud && cd history_cloud
$ source bin/activate
$ pip install jinja2
$ git clone https://github.com/sjkingo/history_cloud.git
$ cd history_cloud
$ ./tagcloud.py > output.html
$ $BROWSER output.html

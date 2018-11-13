<p align="center">
<img src="https://cdn.kagamiz.com/Geetest3-Crack/geetest.svg" width="300">
</p>

<h3 align="center">Geetest3 Distributed Cracking Platform</h3>

## Introduction

This platform works by transferring validation on websites using Geetest to distributed workers which simulate human and auto-complete the process.

A user requests a captcha from a website and submit it to the server, then the cracking task will be randomly assigned to an online worker. The worker will perform sliding puzzle automatically and pass the 2-step verification data back to the user. Post the 2FA data to the website and the validation flow is completed.

*Learn more about [Geetest Networking Sequence](https://docs.geetest.com/static/install/overview/imgs/geetest_netwoking_sequence.jpg)*

## Demo

<video width="800" controls>
<source src="https://cdn.kagamiz.com/Geetest3-Crack/demo.mp4" type="video/mp4">
</video>

## Quick Start

1. Clone or [Download](https://github.com/Hsury/Geetest3-Crack/archive/master.zip) this repository

2. Install [Chrome](https://www.google.com/chrome/) and [ChromeDriver](http://chromedriver.chromium.org/), make sure they can be found in PATH variable

3. Use pip to install requirements

```
python3.6 -m pip install flask gevent pillow requests selenium toml
```

4. Launch [run.py](https://github.com/Hsury/Geetest3-Crack/blob/master/run.py) to test the platform

```
python3.6 run.py
```

## API

Use GET method to access API, and the return data is in JSON format

### /crack

#### Param

- gt

- challenge

- success (Optional, default value is 1)

```
http://127.0.0.1:3333/crack?gt=d712df3d362b20bd5b3d290adf7603bc&challenge=dbd7e4f6318d3338f9e698875ecc3a56&success=1
```

#### Return

- Success

```
{'code': 0, 'message': 'success', 'challenge': 'dbd7e4f6318d3338f9e698875ecc3a5637', 'validate': 'f5d49c5f0a0f5a9dd8a65aef3416737a', 'seccode': 'f5d49c5f0a0f5a9dd8a65aef3416737a|jordan'}
```

- Invalid parameter

```
{'code': -1, 'message': 'invalid parameter'}
```

- Error

```
{'code': -2, 'message': 'error'}
```

- Timeout

```
{'code': -3, 'message': 'timeout'}
```

### /status

#### Param

None

```
http://127.0.0.1:3333/status
```

#### Return

```
{'code': 0, 'workers': 1, 'pending': 0, 'doing': 1, 'done': 39}
```

*Refer to [demo.py](https://github.com/Hsury/Geetest3-Crack/blob/master/demo.py) for more examples*

## Disclaimer

The project is for study and technical communication only, do not use it for illegal purposes

I don't take any responsibility if legal dispute occurs

## License

Geetest3 Distributed Cracking Platform is under The Star And Thank Author License (SATA)

This project is released based on the MIT protocol and adds the SATA protocol

You are obliged to like this open source project and consider giving the author an appropriate reward ∠( ᐛ 」∠)＿

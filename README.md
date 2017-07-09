# modern-blockfolio

A tool to simplify investments in a diversified portfolio of blockchain coins and tokes.

## Idea

Investing in more than a couple of different blockchain assets can be quite tedious, especially when some are only traded in bitcoin or ether but not in fiat currencies. The idea of this python tool is to help you invest into a blockchain portfolio following a predefined asset allocation. Once complete, it shall support three different actions. All of them try to rebalance the portfolio to its original asset allocation as much as possible:

* Deposits
* Rebalance
* Withdrawals

## Dependencies

The few dependencies are [Python3](https://www.python.org/download/releases/3.0/) and a couple of python packages. It helps to set up a [virtualenv](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/) first. The following instructions assume that you have already installed Python which nowadays comes automatically with pip. Start with installing virtualenv and then create a virtual environment in this folder:

```sh
pip install virtualenv
virtualenv -p python3 .venv
```

Now activate the virtual environment with:

```sh
source .venv/bin/activate
```

Finally install the python packages with pip and you are good to go:

```sh
pip install -r requirements.txt
```

## Tests

Run pytest through the proper python binary in the virtualenv:

```sh
python -m pytest
```

## Running the code

Copy the `sample_data` folder, name the copy `data` and adjust the `blockfolio.yaml` file to your needs.

As of now, the code is very simple and only works for one specific use case. That use case is when you have extra funding in your preferred fiat currency available and you also plan on buying more of all of your current holdings.

The code then prints the buy actions and sometimes asks how much of an asset you just bought. It also includes instructions for when you need to transfer assets from one exchange to another one.

Run the code with:

```sh
python main.py [-h] {deposit,withdraw} amount
```

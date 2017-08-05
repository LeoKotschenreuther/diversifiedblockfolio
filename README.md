# Diversified Blockfolio

A tool to simplify investments in a diversified portfolio of blockchain assets.

## Idea

Investing in more than a couple of different blockchain assets can be quite tedious, especially when some of them are not traded in fiat currencies. The idea of this python tool is to help you invest into a blockchain portfolio following a predefined asset allocation. Once complete, it shall support three main actions. All of them try to rebalance the portfolio to its original asset allocation as much as possible:

* Deposits
* Rebalance
* Withdrawals

## Dependencies

The few dependencies are [Python3](https://www.python.org/download/releases/3.0/) and a couple of python packages. It helps to set up a [virtualenv](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/) first. The following instructions assume that you have already installed Python and pip. Start with installing virtualenv and then create a virtual environment in this folder:

```sh
pip install virtualenv
virtualenv -p python3 .venv
```

Now activate the virtual environment with:

```sh
source .venv/bin/activate
```

Finally install the python packages with pip:

```sh
pip install -r requirements.txt
```

## Tests

Run pytest as a python module after having activated the virtualenv:

```sh
python -m pytest
```

## Running the code

Copy the `sample_data/blockfolio.yaml` file to a location of your choice. The default location of the `blockfolio.yaml` file is `data/blockfolio.yaml` but you can specify the actual location when running the `main.py` script with the `--DATAFILE` argument.

As of now, there are only two methods actually implemented, they are for displaying the total value of the holdings in USD and the actual holdings.

Run the code with:

```sh
python main.py [-h] [-d DATAFILE] {holdings,value}
```

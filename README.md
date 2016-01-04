# Swedbank wrapper for python

## Notice
Swedbank will eventually remove password login, there will be changes on how to use this when that happen.

## Usage

    $pip install pyswedbank
    $swedbank-cli [options]
    
    Options:
      -h, --help            show this help message and exit
      -u username, --username=username
                            Username
      -p passwd, --password=passwd
                            Password
      -b bank, --bank=bank  Choose which bank you want to use. Default first bank
      -B, --list-banks      List banks to choose from
      -t, --transactions    Show all available transactions for account.

## Future
There will be work done to make this more library like. EX:

    >>> from pyswedbank import Swedank
    >>> swe = Swedbank(username, password='password')
    >>> print(swe.list_accounts())
    {'account1 name': 1500000.4, 'account2 name': 1200000.4}  # Money!!!
    >>> acc = swe.get_account('account1 name')
    >>> print(acc.amount())
    1500000.4
    

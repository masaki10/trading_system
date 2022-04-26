## Trading system for index fund, stock, bond and so on.

### Setup
create config.py and write config setting to it 

```
CHANNEL_ACCESS_TOKEN = ""

CHANNEL_SECRET = ""

USER_ID = ""

RAKUTEN_ID = ""

RAKUTEN_PASSWORD = ""

ORDER_PASS = ""

FUND_URL = ""
RATE = 
PRICE = 
```

create venv environment and install library

```
python -m venv <environment name>
source <environment name>/bin/activate
pip install -r requirements.txt
```

run trading system 

```
cd trading_system
python main.py
```

### TODO
- deploy and run trading with using line
- manage multiple funds
- optimize portfolio
# Amazon Price Notification
Receive notifications from price changes in your Amazon wishlists as frequently as required.

# Config
Rename config.rename.py to config.py and replace with your own values.

## Price Changes
By default if the change is +-5% you will be notified. Change this in config, `PRICE_CHANGE_DEFAULT_PCT`


## Price Match
Once the main runs, it will produce a json file in the data folder. Copy the items along with the prices you desire in the pricematch.json file to receive notifications on those items as well.

## New Prices
If the item returns to Amazon you will be notified.

# Email output

 - Price comparisons
 - Historical chart data
 - Product image

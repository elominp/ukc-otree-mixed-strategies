## Object hierarchy

```
Session
    Subsession
        Group
            Player
                Page
```

- A session is a series of subsessions
- A subsession contains multiple groups
- A group contains multiple players
- Each player proceeds through multiple pages

## Model fields

Here are the main field types:

- BooleanField (for true/false and yes/no values)
- CurrencyField for currency amounts; see Money & Payoffs.
- IntegerField
- FloatField (for real numbers)
- StringField (for text strings)
- LongStringField (for long text strings)

## Constants

The Constants class is the recommended place to put your app’s parameters and constants that do not vary from player to player.

Here are the required constants:

    name_in_url: the name used to identify your app in the participant’s URL.

    For example, if you set it to public_goods, a participant’s URL might look like this:

    http://otree-demo.herokuapp.com/p/zuzepona/public_goods/Introduction/1/

    players_per_group (described in Groups)

    num_rounds (described in Rounds)

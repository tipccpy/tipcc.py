## installing:
```python
pip install tipcc --upgrade
```

## stuff for me to work on:

- tipping does not work for whatever reason even though (i think) i followed everything the docs said.... gives 415 error (wrong media type)
- some requests are very peculiar about how the currency is specified "Bitcoin", "bitcoin", "btc", "sat" - need to make it convert it
- need to write some docs

## Contributing
Clone the repo and set up a [virtual environment](https://docs.python.org/3/library/venv.html) where tipcc.py is:

```
python -m venv .venv
```

Then install dependencies using:

```
pip install -r requirements.txt
```

You're now ready to add new changes and test the code using this virtual enviroment.
This is to avoid dependency version differences between developers.

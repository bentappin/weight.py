weight.py
=========

Weight helper class for Python it can be used to store and convert between weights.

Example
-------

```
>>> from weight import Weight
>>> me = Weight(st=13)
>>> me
Weight(st=13.0)
>>> me.kg
82.55381134000001

>>> new_me = me - Weight(kg=5)
>>> new_me
Weight(st=12.2126347779)
>>> new_me.kg
77.55381134000001
>>> new_me.st_lbs
(12.0, 2.9768868907561341)
```

Credit
------

This is a port of the geodjango Distance class. Much credit belongs to the original authors.
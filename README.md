# Exercise 2

## Part 1

-   Use `from Part1 import *` to import the `User` and `Item` classes, and the `get_profiles(inputfile)` function.
-   `get_profiles` returns a dictionary with keys `users` and `items`.

### Example

Running the code below:

```python
from Part1 import *

profiles = get_profiles('movielens.txt')
user_profiles = profiles['users']
item_profiles = profiles['items']

print user_profiles[0]

print item_profiles[0]
```

Will result in:

    +----------+----------+
    |      User 614       |
    +----------+----------+
    |   Item   |  Rating  |
    +----------+----------+
    |    1     |    5     |
    +----------+----------+
    |    7     |    2     |
    +----------+----------+
    |    9     |    4     |
    +----------+----------+
    |    14    |    3     |
    +----------+----------+
    |    25    |    1     |
               .
               .
               .
    |   1142   |    3     |
    +----------+----------+
    
    +----------+----------+
    |      Item 1515      |
    +----------+----------+
    |   User   |  Rating  |
    +----------+----------+
    |   308    |    4     |
    +----------+----------+

## Part 2

-   To Be Luvtonized

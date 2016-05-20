# Part 1

-   Use `from Part1 import *` to import the `User`, `Item`, and `Profiles` classes.
-   Use `Profiles.create(input_file)` to get the initial data.
-   Given an instance of `Profiles`, `ps`, use `ps.get_*_by_id` (where \* can be either `user` or `item`) to get instances of `User` and `Item`, or `None` if no such object exists.

## Example

Running the code below:

```python
from Part1 import *

profiles = Profiles.create('movielens.txt')
user_7 = profiles.get_user_by_id(7)
item_341 = profiles.get_item_by_id(341)

item_341.pretty_print()

print 'Rating of item 341 by user 688: %s' % item_341.get_rating_by_id(688)
# Rating of item 101 by user 5 can also be achieved by:
# user_688.get_rating_by_id(341)
```


Will result in:

    +----------+----------+
    |      Item 341       |
    +----------+----------+
    |   User   |  Rating  |
    +----------+----------+
    |    7     |    3     |
    +----------+----------+
    |    8     |    2     |
    +----------+----------+
    |   351    |    4     |
    +----------+----------+
    |   405    |    1     |
    +----------+----------+
    |   485    |    4     |
    +----------+----------+
    |   634    |    2     |
    +----------+----------+
    |   688    |    5     |
    +----------+----------+
    
    Rating of item 341 by user 688: 5

# Part 2

-   To Be Luvtonized

import csv
import sys

from itertools import groupby
from operator import itemgetter
from sklearn.cross_validation import train_test_split

__all__ = ['User', 'Item', 'Profiles']


class Profiles(object):
    @staticmethod
    def create(input_file):
        data = _get_content(input_file)
        return Profiles(_fold_by_column(data, 0, User), _fold_by_column(data, 1, Item))

    def __init__(self, users, items):
        self._users = users
        self._items = items

    def split_20_80(self):
        seed = 1337
        return train_test_split(self._users, test_size=0.8, random_state=seed)

    def get_user_by_id(self, id_):
        return self._get_by_id('users', id_)

    def get_item_by_id(self, id_):
        return self._get_by_id('items', id_)

    def _get_by_id(self, attr, id_):
        for e in getattr(self, '_%s' % attr):
            if e.id == id_:
                return e
        return None


class Ratable(object):
    def __init__(self, id_, ratings):
        self._id = id_
        self.ratings = ratings

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.id == self.id

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.__dict__)

    def pretty_print(self):
        top = '| {:^19} |\n'.format('%s %s' % (self.__class__.__name__, self.id))
        headers = '| {:^8} | {:^8} |\n'.format(self._extra_attr().capitalize()[:-1], 'Rating')
        sep = '+-{0}-+-{0}-+\n'.format('-' * 8)
        content = sep + headers + sep
        for a, r in self._attr_rating_pairs():
            content += '| {:^8} | {:^8} |\n'.format(a, r)
            content += sep
        print sep + top + content

    def _attr_rating_pairs(self):
        return zip(getattr(self, self._extra_attr()), self.ratings)

    def _extra_attr(self):
        return list(set(self.__dict__.keys()) - {'_id', 'ratings'})[0]

    def get_rating_by_id(self, id_):
        for eid, r in self._attr_rating_pairs():
            if eid == id_:
                return r
        return None

    @property
    def id(self):
        return self._id


class User(Ratable):
    def __init__(self, id_, ratings, items):
        super(User, self).__init__(id_, ratings)
        self.items = items


class Item(Ratable):
    def __init__(self, id_, ratings, users):
        super(Item, self).__init__(id_, ratings)
        self.users = users


def _get_content(input_file):
    with open(input_file, 'rb') as f:
        reader = csv.reader(f, dialect='excel-tab')
        return [[int(e) for e in line] for line in reader]


def _fold_by_column(data, idx, cls):
    sorted_by_column = sorted(data, key=itemgetter(idx))
    objects = set()
    for id_, entries in groupby(sorted_by_column, key=itemgetter(idx)):
        items_or_users, ratings = zip(*[(row[1-idx], row[2]) for row in entries])
        objects.add(cls(id_, list(ratings), list(items_or_users)))
    return list(objects)


def _write_to_csv(profiles, attr, filename):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        for profile in profiles:
            writer.writerow([profile.id] + [getattr(profile, attr)] + [profile.ratings])


def main():
    if len(sys.argv) != 5 or sys.argv[1] != 'ExtractProfiles':
        print ('usage: python Part1.py ExtractProfiles '
               '<rating_input_file> <user_profile_output_dir> <item_profile_output_dir>')
        sys.exit(1)
    input_file, user_profiles_file, item_profiles_file = sys.argv[2:]
    print 'Reading file ...',
    data = _get_content(input_file)
    print 'DONE'
    print 'Creating user profiles ...',
    users = _fold_by_column(data, 0, User)
    print 'DONE'
    print 'Creating item profiles ...',
    items = _fold_by_column(data, 1, Item)
    print 'DONE'
    print "Writing '%s' ..." % user_profiles_file,
    _write_to_csv(users, 'items', user_profiles_file)
    print 'DONE'
    print "Writing '%s' ..." % item_profiles_file,
    _write_to_csv(items, 'users', item_profiles_file)
    print 'DONE'
    print 'SUCCESS! :-)'


if __name__ == '__main__':
    main()

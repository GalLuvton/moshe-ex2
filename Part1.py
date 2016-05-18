import csv
import sys

from itertools import groupby
from operator import itemgetter

__all__ = ['User', 'Item', 'get_profiles']


class Ratable(object):
    def __init__(self, id_, ratings):
        self._id = id_
        self.ratings = ratings

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.id == self.id

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.__dict__)

    def __str__(self):
        top = '| {:^19} |\n'.format('%s %s' % (self.__class__.__name__, self.id))
        extra_attr = list(set(self.__dict__.keys()) - {'_id', 'ratings'})[0]
        extra_attr_singular_capitalized = extra_attr.capitalize()[:-1]
        headers = '| {:^8} | {:^8} |\n'.format(extra_attr_singular_capitalized, 'Rating')
        sep = '+-{0}-+-{0}-+\n'.format('-' * 8)
        content = sep + headers + sep
        for a, r in zip(getattr(self, extra_attr), self.ratings):
            content += '| {:^8} | {:^8} |\n'.format(a, r)
            content += sep
        return sep + top + content

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


def get_profiles(input_file):
    data = _get_content(input_file)
    return {'users': _fold_by_column(data, 0, User),
            'items': _fold_by_column(data, 1, Item)}


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

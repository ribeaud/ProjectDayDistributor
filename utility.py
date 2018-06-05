from itertools import repeat

def fill(length, value):
    return list(repeat(value, length))

def sort_students(students):
    '''
    Sorts students by their level first (and if present), then by their name
    '''
    def by_level_then_name(stu1, stu2):
        if hasattr(stu1, 'level'):
            assert hasattr(stu2, 'level'), "Must have attribute 'level' as well"
            prepend = 'schule-'
            l1 = stu1.level[stu1.level.index(prepend):]
            l2 = stu2.level[stu2.level.index(prepend):]
            return cmp(natsort_key(l1), natsort_key(l2)) or cmp(stu1.name, stu2.name)
        else:
            return cmp(stu1.name, stu2.name)

    return sorted(students, cmp=by_level_then_name)

def natsort_key(s):
    '''
    Used internally to get a tuple by which s is sorted.
    '''
    import re
    def try_int(s):
        "Convert to integer if possible."
        try: return int(s)
        except: return s
    return map(try_int, re.findall(r'(\d+|\D+)', s))

import unicodecsv as _csv

def is_comment(line):
    return line.startswith('#')

def is_empty(line):
    return len(line) == 0

def iter_filtered(in_file, *filters):
    for line in in_file:
        line = line.strip()
        if not any(fltr(line) for fltr in filters):
            yield line

# A dis-advantage of this approach is that it requires storing rows in RAM
# However, the largest CSV files I worked with were all under 100 Mb
def read_and_filter_csv(csv_path, *filters):
    with open(csv_path, 'r') as fin:
        iter_clean_lines = iter_filtered(fin, *filters)
        reader = _csv.DictReader(iter_clean_lines, delimiter='\t')
        return [row for row in reader]

def default_read_and_filter_csv(csv_path):
    return read_and_filter_csv(csv_path, is_comment, is_empty)
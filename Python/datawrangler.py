"""Data wrangling helper functions."""
import csv
import glob
import os


class excel_semicolon(csv.excel):
    """here you can set the parameters of your csv."""

    delimiter = ';'


# register the delimeter
csv.register_dialect("excel-semicolon", excel_semicolon)


def getDialect(filename):
    """Get the dialect of the given csv file."""
    with open(filename, 'rb') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
    return dialect


def getDialects(filenames):
    """Get the dialect of the first of the given csv files."""
    return getDialect(filenames[0])


def getCSVFilesFromFolder(folder_name):
    """Get all files from the specified folder."""
    all_files = glob.glob(os.path.join(folder_name, "*.csv"))
    return all_files


def getColumnNames(filenames, dialect=None):
    """Get a set of column names of the files."""
    if dialect is None:
        dialect = getDialects(filenames)

    column_names = set()
    for filename in filenames:
        with open(filename, "rb") as f_in:
            reader = csv.reader(f_in, dialect=dialect)
            headers = next(reader)
            for h in headers:
                column_names.add(h)
    return column_names


def getFileLength(filename):
    """Get the number of lines of a file."""
    lines = 0
    for line in open(filename):
        lines += 1
    return lines


def splitCSV(source, targets, dialect=None):
    """Split the source file at the specified position into two files."""
    num_lines = getFileLength(source) - 1
    if num_lines < 2:
        raise OSError("File has too less lines to split")

    lines_target = round(num_lines / len(targets))

    if dialect is None:
        dialect = getDialect(source)

    with open(source, 'rb') as inp:
        reader = csv.reader(inp, dialect=dialect)

        # first get the header
        column_names = next(reader)
        process = 0
        for target in targets:
            with open(target, 'wb') as out:
                writer = csv.writer(out, dialect=dialect)
                # first write the header
                writer.writerow(column_names)
                # then write the next lines for this file
                row_number = 0
                while row_number < lines_target:
                    read_row = next(reader)
                    writer.writerow(read_row)
                    row_number += 1
                    process += 1
                    # output progress:
                    if process % 1000 == 0:
                        print(str(process) + " lines copied (" +
                              str(round(100 * process / num_lines)) + "%)")


def getIndicesOfNames(names_short, names_all):
    """Get the indices of the names of the first list in the second list.

    names_short
        is the first list
    names_all
        is the second list
    Returns
        a list of tuples with the index of the occurence in the list names_all
        and the name
    """
    indices = []
    for count, name in enumerate(names_short):
        if name:
            matches = [(s, i)
                       for i, s in enumerate(names_all) if name in s]
            if len(matches) == 0:
                print("Did not found " + name)
            elif len(matches) == 1:
                indices.append((count, matches[0][1]))
            else:
                print("Multiple matches for " + name + ":")
                for m in matches:
                    indices.append((count, m[1]))
    return indices


def mergeCSVs(source_filenames, target_filename, dialect=None):
    """Merge the two source files into one file.

    It is assumed that all source files use the same dialect
    """
    if dialect is None:
        dialect = getDialects(source_filenames)

    column_names = getColumnNames(source_filenames)

    # debug parameters
    file_iter = 1
    num_files = len(source_filenames)

    # Then copy the data
    with open(target_filename, "wb") as f_out:
        writer = csv.DictWriter(
            f_out, fieldnames=column_names, dialect=dialect)
        writer.writeheader()
        for filename in source_filenames:
            with open(filename, "rb") as f_in:
                # Uses the field names in this file
                reader = csv.DictReader(f_in, dialect=dialect)
                for line in reader:
                    # At this point, line is a dict with the field names as
                    # keys, and the column data as values.
                    # You can specify what to do with blank or unknown values
                    # in the DictReader and DictWriter constructors.
                    writer.writerow(line)
            print("Merged: %d/%d Files" % (file_iter, num_files))
            file_iter = file_iter + 1


def csvLazyGet(filename, dialect=None):
    """Yield the rows of a file."""
    if dialect is None:
        dialect = getDialect(filename)

    with open(filename) as f:
        r = csv.reader(f, dialect=dialect)
        for row in r:
            yield row


def areEqualCSV(filenames):
    """Check if the files of a list of names are equal."""
    gen_2 = csvLazyGet(filenames[0])

    are_equal = True

    for filename in filenames[1:]:
        for row_1 in csvLazyGet(filename):
            row_2 = gen_2.next()

            are_equal = set(row_2) == set(row_1)
            if not are_equal:
                print("rows from %s and %s are not equal." %
                      (filenames[0], filename))
                print(row_1)
                print(row_2)
                break
        if not are_equal:
            break

    gen_2.close()

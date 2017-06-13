"""Data wrangling helper functions."""
import csv


class excel_semicolon(csv.excel):
    """here you can set the parameters of your csv."""

    delimiter = ';'


# register the delimeter
csv.register_dialect("excel-semicolon", excel_semicolon)


def getDialect(source):
    """Get the dialect of the given csv file."""
    with open(source, 'rb') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
    return dialect


def getColumnNames(source, dialect=None):
    """Get the column names of the big file as a list."""
    if dialect is None:
        dialect = getDialect(source)
    column_names = []
    with open(source, "rb") as f_in:
        reader = csv.reader(f_in, dialect=dialect)
        column_names = next(reader)
    return column_names


def getFileLength(filename):
    """Get the number of lines of a file"""
    lines = 0
    for line in open(filename):
        lines += 1
    return lines


def split_csv(source, target_1, target_2, split=0.5, dialect=None):
    """Split the source file at the specified position into two files."""
    num_lines = getFileLength(source) - 1
    if num_lines < 2:
        raise OSError("File has too less lines to split")

    lines_target_1 = round(num_lines * split)

    if dialect is None:
        dialect = getDialect(source)

    with open(source, 'rb') as inp, \
            open(target_1, 'wb') as out_1, \
            open(target_2, 'wb') as out_2:
        writer_1 = csv.writer(out_1, dialect=dialect)
        writer_2 = csv.writer(out_2, dialect=dialect)
        reader = csv.reader(inp, dialect=dialect)
        # first write the headers (to both files)
        column_names = next(reader)
        writer_1.writerow(column_names)
        writer_2.writerow(column_names)

        row_number = 0
        for read_row in reader:
            row_number += 1
            if row_number < lines_target_1:
                writer_1.writerow(read_row)
            else:
                writer_2.writerow(read_row)

            # output progress:
            if row_number % 1000 == 0:
                print(str(row_number) + " lines copied (" +
                      str(round(100 * row_number / num_lines)) + "%)")

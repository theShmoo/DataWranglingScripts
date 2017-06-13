"""Helpers for the infineon data set."""
import csv
import re
from datetime import datetime
import datawrangler as dw


# stuff to remove from column names
removes_from_column_name = ["dist_2.COMPRESSED_INF_", ".COMP_30_SEC"]


def shortenColumnNames(column_names):
    """Use a set of words that are removed from the list of names."""
    short_names = []
    for name in column_names:
        h = name
        for rem in removes_from_column_name:
            h = h.replace(rem, "")
        short_names.append(h)
    return short_names


def getIndicesOfColumnNames(names, column_names):
    """Get the indices of the names of the first list in the second list."""
    indices = []
    for count, name in enumerate(names):
        if name:
            matches = [(s, i)
                       for i, s in enumerate(column_names) if name in s]
            if len(matches) == 0:
                print("Did not found " + name)
            elif len(matches) == 1:
                indices.append((count, matches[0][1]))
            else:
                filtered_matches = []
                for m in matches:
                    if "__" in m[0]:
                        print("Did not took: " + m[0] + ", because of \"__\"")
                        continue
                    elif "_abs_" in m[0]:
                        print("Did not took: " + m[0] + ", because of \"abs\"")
                        continue
                    elif re.match(r'.*(' + re.escape(name) + ')[0-9].*', m[0]):
                        print("Did not took: " + m[0] + ", because of number")
                        continue
                    else:
                        filtered_matches.append(m)

                if len(filtered_matches) == 0:
                    print("did not found any matches for " + name)
                elif len(filtered_matches) > 1:
                    print("Multiple matches for " + name + ":")
                for m in filtered_matches:
                    if len(filtered_matches) > 1:
                        print("\tfound " + str(m[0]) + " index " + str(m[1]))
                    indices.append((count, m[1]))
    return indices


def mapFromTo(from_indices, to_indices):
    """Get a map from old index to new index."""
    # if no old index exists map from new to new
    from_to = {}
    # magic mapping function:
    for t in to_indices:
        match = [f[1] for f in from_indices if f[0] is t[0]]
        if len(match) == 1:
            from_to[match[0]] = t[1]
        elif len(match) > 1:
            print("Found multiple indices of " + str(t) + ": " + str(match))
        else:
            print("Did not found index " + str(t) + "added mapping new to new")
            from_to[t[1]] = t[1]
    return from_to


def getInfo(source, skip_header, dialect=None):
    """Get the meta info from the file as a list."""
    if dialect is None:
        dialect = dw.getDialect(source)
    important_info = []
    with open(source, "rb") as f_in:
        reader = csv.reader(f_in, dialect=dialect)
        if skip_header:
            # skip the header
            next(reader, None)
        # get ALL the important info!
        for line in reader:
            important_info.append(line)

    return important_info


def modifyHeaderLine(header, important_indices, important_info):
    """Modify the given header line by the important info."""
    header_with_tags = []
    important_iter = iter(important_indices)
    next_important_index = next(important_iter)
    info_count = 0

    # iterate over the header of the original file
    for count, h in enumerate(header):
        column_tags = ""
        if count == next_important_index:
            # get the column tags of the important columns file
            for tag in important_info[info_count][2:]:
                column_tags += "{" + tag + "}"
            # advance the iterators of the important indices
            print(str(count) + " " + str(info_count) + " " + column_tags)
            next_important_index = next(important_iter, -1)
            info_count = info_count + 1

        # refine the column name
        for rem in removes_from_column_name:
            h = h.replace(rem, "")

        # prepend the column tag to the column name
        header_with_tags.append(column_tags + h)

    return header_with_tags


def getMulitples(indices):
    """Return a subset with no multiples (filters out the bad ones)."""
    multiples = []
    added = []
    for i in range(0, len(indices) - 1):
        if indices[i][0] == indices[i + 1][0]:
            added.append(indices[i])
        elif added:
            added.append(indices[i])
            multiples.append(added)
            added = []

    return multiples


def parseTime(date_str):
    """Return a datetime from the infineon string."""
    # (format: 01.03.2017 13:24:30)
    return datetime.strptime(date_str, '%d.%m.%Y %H:%M:%S')

import re


def convert_to_raw_tsquery(query):
    words = query.split()
    prefixed_words = (u'%s:*' % word for word in words)
    return u' & '.join(prefixed_words)


def _split_query(query):
    """
    Splits a query in pieces like so:

    - if the query looks like a phone number, join the numbers together
    - if double quotes are used, keep those parts together
    - split the rest into words

    :param str query: the query to split

    :returns: the pieces of the query
    :rtype: list
    """
    if re.match(r'^[0-9\.\+\s]+$', query):
        return  [ re.sub(r'\s', '', query) ]

    else:
        return map(lambda p: p.strip('"'), re.compile('[^ "]+|"[^"]+"').findall(query))


def preprocess_full_text_query(q, exact=False):
    """
    Preprocesses a query like so:

    - split into pieces
    - add wildcards to it (when not using exact matching)
    - join the query with wildcards back together

    :param str q: the query to process
    :param bool exact: whether exact matching should be used

    :returns: the processed query
    :rtype: str
    """
    def add_wildcards(part):
        # Don't know why, but '@' characters cause weird behaviour and are not indexed anyway.
        part = part.replace('@', ' ')

        # For an exact match: no wildcards, but double quotes
        if exact:
            return '+"%s"' % part

        # For a part containing wildcards already, don't quote or insert own wildcards.
        elif '*' in part:
            return '+%s' % part

        # Any spaces in this part?
        elif ' ' in part:
            return '+"%s"*' % part

        # Otherwise, append *
        else:
            return '+%s*' % part

    return ' '.join(map(add_wildcards, _split_query(q)))

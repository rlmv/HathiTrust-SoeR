
import argparse
from string import lower

from marc import MarcSQLite, get_id_from_record


def has_reference(record):
    for field in record.subjects():
        try:
            subj = lower(field.get_subfields('a')[0])   
            for term in terms:
                if term in subj:
                    return True
        except IndexError:
            pass
    return False


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")
    parser.add_argument('MARCDB',
                        help='MarcSQLite database from which to retrieve records.')
    parser.add_argument('TERM',
                        nargs='+',
                        help='Terms signalling positive identification.')
    parser.add_argument('--out', 
                        help='Optional file to write output to.')

    args = parser.parse_args()

    terms = [lower(s) for s in args.TERM]

    m = MarcSQLite(args.MARCDB)

    with open(args.out, 'w') as f_id:

        with m:
            for r in m.get_all_records():
                if has_reference(r):
                    id_ = get_id_from_record(r)
                    print id_
                    f_id.write("{}\n".format(id_))
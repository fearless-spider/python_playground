import csv


def reader():
    with open("../emails/loh_cleaned.csv") as csvfile:
        csv_gen = csv.reader(csvfile)
        row_count = 0

        for row in csv_gen:
            row_count += 1

        print(f"Row count is {row_count}")


def csvopen():
    for row in open("../emails/loh_cleaned.csv", "r"):
        yield row


def csvgen():
    return (row for row in open("../emails/loh_cleaned.csv"))


def reader_yield():
    csv_gen = csvopen()
    row_count = 0

    for row in csv_gen:
        row_count += 1

    print(f"Row count is {row_count}")


def reader_gen():
    csv_gen = csvgen()
    row_count = 0

    for row in csv_gen:
        row_count += 1

    print(f"Row count is {row_count}")


reader_gen()

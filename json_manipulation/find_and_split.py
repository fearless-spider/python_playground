if __name__ == '__main__':
    f = open('combined_errors.json-error', 'r')
    lines = f.readlines()

    date_error = []
    for line in lines:
        if 'Date is in the past' in line:
            date_error.append(line)

    sub_error = []
    for line in lines:
        if 'migrate_subscription - Subscription' in line:
            sub_error.append(line)

    print(len(lines))
    print(len(date_error))
    print(len(sub_error))
    other_errors = []
    for line in lines:
        if line not in date_error and line not in sub_error:
            other_errors.append(line)
    print(len(other_errors))

    f_o = open('other_error.json-error', 'w')
    f_o.writelines(other_errors)
    f_o.close()

    f_e = open('date_error.json-error', 'w')
    f_e.writelines(date_error)
    f_e.close()

    f_s = open('subscription_error.json-error', 'w')
    f_s.writelines(sub_error)
    f_s.close()
    f.close()

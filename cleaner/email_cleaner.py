from pymongo import MongoClient, DESCENDING
import requests
import json
import datetime


def clear_emails():
    # connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client.wolf
    # Issue the serverStatus command and print the results
    serverStatusResult = db.command("serverStatus")
    print(serverStatusResult)
    print(db.collection_names())

    emails = db.optoutemails.find({'_deleted_in_mautic': None}).sort([('_created', DESCENDING)])
    print(emails.count())

    for email in emails[0:10]:
        email_name = email.get('email')
        print(email_name)
        r = requests.get("http:///mautic/api/contacts?search=email:" + email_name, auth=("",""))
        print(r.status_code)
        if r.status_code == 200:
            data = r.json()
            for contact in data.get('contacts'):
                print(contact)
                r2 = requests.post("http:///mautic/api/contacts/" + contact + "/dnc/email/add", auth=("",""))
                print(r2.status_code)
        result = db.optoutemails.update_one({'_id': email.get('_id')}, {'$set':{'_deleted_in_mautic': datetime.datetime.utcnow()}})

        print('Number of documents modified : ' + str(result.modified_count))

    client.close()

if __name__ == '__main__':
    clear_emails()
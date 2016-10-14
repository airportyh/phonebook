from flask import Flask, render_template, request, redirect
import pg

db = pg.DB(dbname='phonebook')

app = Flask('phone book v4')

@app.route('/')
def list_entries():
    entries = db.query('select * from phonebook').namedresult()
    return render_template(
        'list_entries.html',
        title='All Entries',
        entries=entries
    )

@app.route('/new_entry')
def new_entry():
    return render_template(
        'new_entry.html',
        title='Add Entry'
    )

@app.route('/submit_new_entry', methods=['POST'])
def submit_new_entry():
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    db.insert('phonebook',
        name=name,
        phone_number=phone_number,
        email=email)
    return redirect('/')

@app.route('/update_entry')
def update_entry():
    id = int(request.args.get('id'))
    query = db.query('''
    select * from phonebook
    where id = %d''' % id)
    entry = query.namedresult()[0]
    return render_template(
        'update_entry.html',
        entry=entry
    )

@app.route('/submit_update_entry', methods=['POST'])
def submit_update_entry():
    id = int(request.form.get('id'))
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    action = request.form.get('action')
    if action == 'update':
        db.update('phonebook', {
            'id': id,
            'name': name,
            'phone_number': phone_number,
            'email': email
        })
    elif action == 'delete':
        db.delete('phonebook', { 'id': id })
    else:
        raise Exception("I don know how to %s" % action)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

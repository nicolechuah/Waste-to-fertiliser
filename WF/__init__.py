from flask import Flask, render_template, request, redirect, url_for,session
from Forms import UserFWF
from Fwfuser import FWFUser
import shelve


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html', title = "Products")

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/join-us')
def join_us():
    return render_template('join-us.html')

@app.route('/user_fwf', methods=['GET', 'POST'])
def fwf_user():
    fwf_user_form = UserFWF(request.form)
    if request.method == 'POST' and fwf_user_form.validate():
        fwfuser_dict = {}
        db = shelve.open('FWFUser.db', 'c')

        try:
            fwfuser_dict = db['FWFUser']
            fwfuser_id = db['FWFUserIDs']
            FWFUser.count_id= fwfuser_id

        except:
            print("Error in retrieving data from FWFUser.db")
        fwfUser = FWFUser(fwf_user_form.first_name.data, fwf_user_form.last_name.data,
                                  fwf_user_form.gender.data, fwf_user_form.email.data, fwf_user_form.remarks.data or '')
        fwfuser_dict[fwfUser.get_fwfuser_id()] = fwfUser
        db['FWFUser'] = fwfuser_dict
        db['FWFUserIDs'] = FWFUser.count_id
        db.close()

        return redirect(url_for('view', fwfuser_id=fwfUser.get_fwfuser_id()))

    return render_template('user_fwf.html', form=fwf_user_form)


@app.route('/regconfirm/<int:fwfuser_id>', methods=['GET'])
def view(fwfuser_id):
    db = shelve.open('FWFUser.db', 'r')
    try:
        fwfuser_dict = db['FWFUser']

        fwfuser = fwfuser_dict.get(fwfuser_id)

        if fwfuser:
            return render_template('regconfirm.html', fwfuser=fwfuser)
        else:
            return f"FWFuser with ID {fwfuser_id} not found."

    except KeyError:
        return "Error: User data not found in the database."

    except Exception as e:
        # Handle any unexpected errors
        print(f"Error retrieving user: {str(e)}")
        return "An error occurred while retrieving the user."

    finally:
        db.close()

@app.route('/Editfwfuser/<int:id>/', methods=['GET', 'POST'])
def edit_fwfuser(id):
    edit_fwfuser_form = UserFWF(request.form)

    if request.method == 'POST' and edit_fwfuser_form.validate():
        db = shelve.open('FWFUser.db', 'w')
        fwfuser_dict = db.get('FWFUser', {})

        fwfuser = fwfuser_dict.get(id)

        if fwfuser:
            fwfuser.set_first_name(edit_fwfuser_form.first_name.data)
            fwfuser.set_last_name(edit_fwfuser_form.last_name.data)
            fwfuser.set_gender(edit_fwfuser_form.gender.data)
            fwfuser.set_email(edit_fwfuser_form.email.data)
            fwfuser.set_remarks(edit_fwfuser_form.remarks.data)

            db['FWFUser'] = fwfuser_dict

        db.close()

        # Redirect to a confirmation or another page after the update
        return redirect(url_for('fwfuser_ADretrieve', fwfuser_id=fwfuser.get_fwfuser_id()))

    else:
        # Open the shelve database in read mode
        db = shelve.open('FWFUser.db', 'r')

        # Retrieve the users' data
        fwfuser_dict = db.get('FWFUser', {})
        db.close()

        # Get the user data using the ID from the URL
        fwfuser = fwfuser_dict.get(id)

        if fwfuser:
            # Populate the form with the current user data
            edit_fwfuser_form.first_name.data = fwfuser.get_first_name()
            edit_fwfuser_form.last_name.data = fwfuser.get_last_name()
            edit_fwfuser_form.gender.data = fwfuser.get_gender()
            edit_fwfuser_form.email.data = fwfuser.get_email()
            edit_fwfuser_form.remarks.data = fwfuser.get_remarks()

        # Pass both the form and the user data to the template
        return render_template('Editfwfuser.html', form=edit_fwfuser_form, fwfuser=fwfuser)
        return redirect(url_for('fwfuser_ADretrieve'))

@app.route('/delete_fwfuser/<int:id>/', methods=['POST'])
def delete_fwfuser(id):
    db = shelve.open('FWFUser.db', 'w')

    # Retrieve the users' data from the database
    fwfuser_dict = db.get('FWFUser', {})


    if id in fwfuser_dict:
        del fwfuser_dict[id]
        db['FWFUser'] = fwfuser_dict

    db.close()

    return redirect(url_for('fwfuser_ADretrieve'))


@app.route('/fwfuser_ADretrieve', methods=['GET'])
def fwfuser_ADretrieve():
    fwfusers_dict ={}
    db = shelve.open('FWFUser.db', 'r')

    fwfusers_dict = db['FWFUser']
    db.close()
    fwfusers_list = []
    for key in fwfusers_dict:
        fwfuser = fwfusers_dict.get(key)
        fwfusers_list.append(fwfuser)

    return render_template('fwfuser_ADretrieve.html', count=len(fwfusers_list), fwfusers_list=fwfusers_list)

if __name__ == '__main__':
    app.run(debug=False)

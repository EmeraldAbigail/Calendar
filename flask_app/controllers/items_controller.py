
from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.item import Item

# Routes for Shopping Items

# Create an Item
@app.route('/create_item', methods=['POST'])
def create_item():
    item_complete = 'Y' if  request.form.get ("item_complete") else 'N'
    data = {
        'item_name': request.form['item_name'],
        'item_complete': item_complete 
    }
    Item.create_item(data)
    return redirect('/items')  # Or redirect to the specific shopping list

# Show Item List 
@app.route('/items')  # Include shopping list ID
def display_items():
    if 'user_id' not in session:
        return redirect('/')
    items = Item.get_all_items()  # Get items for the list
    return render_template('show_items.html', items=items)

# Delete Item
@app.route('/items/<int:item_id>/delete')
def delete_item(item_id):
    data = {
        'id': item_id
    }
    Item.delete_item(data)
    return redirect('/items')  # Or redirect to the specific shopping list

#Display form for Item.html
@app.route('/show/item_form')
def show_item_form():
    return render_template('items.html')
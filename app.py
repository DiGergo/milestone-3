import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.getenv("MONGO_DBNAME")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

# route to home page
@app.route('/')
@app.route('/home')
def get_home():
    return render_template("index.html")

# route to categories page
@app.route('/categories')
def get_categories():
    return render_template("categories.html", categories=mongo.db.categories.find())

# route to recipes page
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", 
    recipes=mongo.db.recipes.find())

# route to view one specific recipe
@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    the_recipe=mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("recipe.html", recipe=the_recipe)

# route for Dessert category
@app.route('/get_desserts')
def get_desserts():
    return render_template("recipes.html", 
    recipes=mongo.db.recipes.find({'category_name': 'Dessert'}))

# route for Fish category
@app.route('/get_fish')
def get_fish():
    return render_template("recipes.html", 
    recipes=mongo.db.recipes.find({'category_name': 'Fish'}))

# route for Pasta category
@app.route('/get_pastas')
def get_pastas():
    return render_template("recipes.html", 
    recipes=mongo.db.recipes.find({'category_name': 'Pasta'}))

# route for Meat category
@app.route('/get_meat')
def get_meat():
    return render_template("recipes.html", 
    recipes=mongo.db.recipes.find({'category_name': 'Meat'}))

# route for salads category
@app.route('/get_salad')
def get_salad():
    return render_template("recipes.html", 
    recipes=mongo.db.recipes.find({'category_name': 'Salad'}))

# route for fruits category
@app.route('/get_fruit')
def get_fruit():
    return render_template("recipes.html", 
    recipes=mongo.db.recipes.find({'category_name': 'Fruit'}))

# function that adds a recipe to the mongo database
@app.route('/add_recipe')
def add_recipe():
    return render_template('add_recipe.html',
    recipes=mongo.db.recipes.find(),
    categories=mongo.db.categories.find(),
    time_to_prep=mongo.db.time_to_prep.find(),
    cost=mongo.db.cost.find())

# route to shop page
@app.route('/shop')   
def get_shop():
    return render_template("shop.html")

# function to edit a specific recipe, also loads the information from database
@app.route('/edit/<recipe_id>')
def get_edit(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('edit.html', recipe=recipe,
    categories=mongo.db.categories.find(),
    time_to_prep=mongo.db.time_to_prep.find(),
    cost=mongo.db.cost.find() )

# function to update that specific edited recipe
@app.route('/update/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    the_recipe=mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    recipes = mongo.db.recipes
    recipes.update({'_id': ObjectId(recipe_id)},
    {
        'recipe_name': request.form.get('recipe_name'),
        'category_name': request.form.get('category_name'),
        'time_to_prepare': request.form.get('time_to_prepare'),
        'uploader': request.form.get('uploader'),
        'instructions': request.form.get('instructions'),
        'comments': request.form.get('comments'),
        'costs': request.form.get('costs'),
        'ingredients': request.form.get('ingredients')
    })
    return render_template("recipe.html", recipe=the_recipe)

# function to delete a specific recipe
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return render_template("categories.html", categories=mongo.db.categories.find())

# function that adds a recipe to the database
@app.route('/insert_recipe', methods=['POST'])
def insert_recipes():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_categories'))
    
if __name__ == '__main__' :
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
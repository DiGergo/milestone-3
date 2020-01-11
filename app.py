import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'recipe_db'
app.config["MONGO_URI"] = 'mongodb+srv://root2019:RooT20i9@myfirstcluster-2yjug.mongodb.net/recipe_db?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
@app.route('/home')
def get_home():
    return render_template("index.html")

@app.route('/categories')
def get_categories():
    return render_template("categories.html", categories=mongo.db.categories.find())

@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", 
    recipes=mongo.db.recipes.find())

@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    the_recipe=mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("recipe.html", recipe=the_recipe)

@app.route('/get_desserts')
def get_desserts():
    return render_template("recipes.html", 
    recipes=mongo.db.recipes.find({'category_name': 'Dessert'}))
    
@app.route('/get_fish')
def get_fish():
    return render_template("recipes.html", 
    recipes=mongo.db.recipes.find({'category_name': 'Fish'}))
    
@app.route('/get_pastas')
def get_pastas():
    return render_template("recipes.html", 
    recipes=mongo.db.recipes.find({'category_name': 'Pasta'}))

@app.route('/get_meat')
def get_meat():
    return render_template("recipes.html", 
    recipes=mongo.db.recipes.find({'category_name': 'Meat'}))

@app.route('/get_salad')
def get_salad():
    return render_template("recipes.html", 
    recipes=mongo.db.recipes.find({'category_name': 'Salad'}))

@app.route('/get_fruit')
def get_fruit():
    return render_template("recipes.html", 
    recipes=mongo.db.recipes.find({'category_name': 'Fruit'}))

@app.route('/add_recipe')
def add_recipe():
    return render_template('add_recipe.html',
    recipes=mongo.db.recipes.find(),
    categories=mongo.db.categories.find(),
    time_to_prep=mongo.db.time_to_prep.find(),
    cost=mongo.db.cost.find())

@app.route('/shop')   
def get_shop():
    return render_template("shop.html")

@app.route('/edit/<recipe_id>')
def get_edit(recipe_id):
    the_recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('edit.html', recipe= the_recipe)

@app.route('/update/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        'recipe_name': request.form['recipe_name'],
        'category_name': request.form['category'],
        'time_to_prepare': request.form['time'],
        'uploader': request.form['uploader'],
        'instructions': request.form['instructions'],
        'comments': request.form['comments'],
        'costs': request.form['cost'],
        'ingredients': request.form['ingredient_1']
    })
    
    return render_template("recipes.html") 

@app.route('/insert_recipe', methods=['POST'])
def insert_recipes():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_categories'))
    
if __name__ == '__main__' :
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
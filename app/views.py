import os
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.http import HttpResponse
from django.db import connection
from .models import product, SoccerPlayer, Slide
from .forms import ProductForm  # Assuming you have a form for the Product
import random
import string
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import pandas as pd
from django.views import View
#from sklearn.datasets import load_iris
#from sklearn.datasets import make_moons
from sklearn.datasets import fetch_california_housing
import matplotlib.pyplot as plt
from django.conf import settings
import seaborn as sns

# Step 3: Data Preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
# Step 4: Model Training and Evaluation
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
# Step 5: Model Interpretation and Insights
import numpy as np
# Step 6: Further Model Tuning (Optional)
from sklearn.ensemble import RandomForestRegressor

def generate_random_location():
    # Randomly choose one of 'AND', 'BAS', 'SAL'
    prefix = random.choice(['AND', 'BAS', 'SAL'])
    
    # Generate a random two-digit number between '01' and '99'
    number_part = '{:02}'.format(random.randint(1, 99))
    
    # Generate a random uppercase letter
    letter_part = random.choice(string.ascii_uppercase)
    
    # Combine all parts to form the location string
    location = f"{prefix}-{number_part}-{letter_part}"
    
    return location

def home(request):
    return render(request, 'app/home.html')

def base(request):
    return render(request, 'app/base.html')

def wiki(request):
    return render(request, 'app/wiki.html')

def links(request):
    return render(request, 'app/links.html')

def careers(request):
    return render(request, 'app/careers.html')

def about(request):
    slides = Slide.objects.all()  # Fetch all slides from database
    return render(request, 'app/about.html', {'slides': slides})

def product_insert(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('product_insert')  # Redirect to a list of products or a success page
    else:
        form = ProductForm()

    return render(request, 'app/product_insert.html', {'form': form})

def db_schema(request):
    schema_data = []

    with connection.cursor() as cursor:
        # Get all table names
        #cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            # Get all column details for the table
            #cursor.execute(f"PRAGMA table_info('{table_name}');")
            cursor.execute(f"SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = '{table_name}';")
            columns = cursor.fetchall()
            schema_data.append({
                'table_name': table_name,
                'columns': columns
            })

    return render(request, 'app/db_schema.html', {'schema_data': schema_data})

def product_list(request):
    products = product.objects.all()  # Query all products from the database
    return render(request, 'app/product_list.html', {'products': products})

def generate_random_sku(length=10):
    """ Generate a random SKU """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def generate_random_product(request):
    """ View to generate random products """
    if request.method == 'POST':
        num_products = int(request.POST.get('num_products', 1))
        for _ in range(num_products):
            products = product(
                sku=generate_random_sku(),
                name=f"Product {random.randint(1, 100)}",
                description="Random description",
                price=random.uniform(10, 1000),  # Adjust as needed
                quantity=random.randint(0, 100),
                location=generate_random_location(),
            )
            products.save()
        #return redirect('generate_products_success', num_products=num_products)
    context = {'request': request}
    products = product.objects.all().order_by('-product_id')  # Query all products from the database
    return render(request, 'app/generate_product.html',{'products': products})

def generate_product_success(request, num_products):
    """ Success page after generating products """
    return render(request, 'app/generate_product_success.html', {'num_products': num_products})

class ShowcaseView(View):
    
    def get(self, request):
        return render(request, 'app/showcase.html')

    def post(self, request):
        colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']
        random_color = random.choice(colors)
        
        return JsonResponse({'color': random_color})
    
def search_players(request):
    query = request.GET.get('q', '')
    results = SoccerPlayer.objects.filter(name__icontains=query) if query else []
    return render(request, 'app/search.html', {'query': query, 'results': results})

def data_page(request):
    # Load the dataset
    california_housing = fetch_california_housing()

    # Create a DataFrame from the dataset
    cal_data = pd.DataFrame(california_housing.data, columns=california_housing.feature_names)
    data = pd.DataFrame(california_housing.data, columns=california_housing.feature_names)
    data['MedHouseVal'] = california_housing.target  # Add the target variable
        
    # Correlation matrix
    corr_matrix = data.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    corr_mat_plot_path = os.path.join(settings.STATICFILES_DIRS[0], 'Correlation_Matrix.png')
    plt.savefig(corr_mat_plot_path)
    plt.close()  # Close the plot to free up memory

    # Pair plot
    sns.pairplot(data, vars=['MedInc', 'AveRooms', 'AveOccup', 'MedHouseVal'])
    plot_path = os.path.join(settings.STATICFILES_DIRS[0], 'pairplot.png')
    plt.savefig(plot_path)
    plt.close()  # Close the plot to free up memory

    # Distribution of the target variable
    plt.figure(figsize=(8, 6))
    sns.histplot(data['MedHouseVal'], bins=30, kde=True)
    plt.title('Distribution of Median House Value')
    plot_path = os.path.join(settings.STATICFILES_DIRS[0], 'Distribution_of_Median_House_Value.png')
    plt.savefig(plot_path)
    plt.close()  # Close the plot to free up memory

    # Step 3: Data Preprocessing

    # Split the data into features and target
    X = data.drop('MedHouseVal', axis=1)
    y = data['MedHouseVal']

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize the feature data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Step 4: Model Training and Evaluation
    
    # Initialize and train the model
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test_scaled)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    #print(f'Mean Squared Error: {mse:.4f}')
    Mean_Squared_Error = _('Mean Squared Error: {mse:.4f}').format(mse=mse)
    #print(f'R^2 Score: {r2:.4f}')
    R2_Score = _('R^2 Score: {r2:.4f}').format(r2=r2)

    # Step 5: Model Interpretation and Insights

    # Coefficients and their corresponding features
    coefficients = pd.DataFrame({
        'Feature': X.columns,
        'Coefficient': model.coef_
    })

    #print(coefficients.sort_values(by='Coefficient', ascending=False))
    coeffic = coefficients.sort_values(by='Coefficient', ascending=False)
    # Convert to JSON format
    coeffic_sorted_df_json = coeffic.to_json(orient='records')

    # Step 6: Further Model Tuning (Optional)


    # Initialize and train a Random Forest model
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # Predict on the test set
    rf_y_pred = rf_model.predict(X_test)

    # Evaluate the Random Forest model
    rf_mse = mean_squared_error(y_test, rf_y_pred)
    rf_r2 = r2_score(y_test, rf_y_pred)

    #print(f'Random Forest Mean Squared Error: {rf_mse:.4f}')
    Random_Forest_Mean_Squared_Error = _('Random Forest Mean Squared Error: {rf_mse:.4f}').format(rf_mse=rf_mse)
    #print(f'Random Forest R^2 Score: {rf_r2:.4f}')
    Random_Forest_R2_Score = _('Random Forest R^2 Score: {rf_r2:.4f}').format(rf_r2=rf_r2)

    # Feature Importance from Random Forest
    rf_feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': rf_model.feature_importances_
    })

    #print(rf_feature_importance.sort_values(by='Importance', ascending=False))
    featureimportance = ''#_(rf_feature_importance.sort_values(by='Importance', ascending=False))

    # Visualizing Feature Importances
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Importance', y='Feature', data=rf_feature_importance.sort_values(by='Importance', ascending=False))
    plt.title('Feature Importance from Random Forest')
    plot_path = os.path.join(settings.STATICFILES_DIRS[0], 'Feature_Importance_from_Random_Forest.png')
    plt.savefig(plot_path)
    plt.close()  # Close the plot to free up memory
    
    
    # Convert DataFrame to HTML
    html_table = cal_data.head(25).to_html(classes='table table-striped table-bordered', index=False)
    context = {
        'cal_housing' : html_table,
        'Correlation_Matrix_url':'/static/Correlation_Matrix.png',
        'Distribution_of_Median_House_Value_url':'/static/Distribution_of_Median_House_Value.png',
        'Feature_Importance_from_Random_Forest_url' : '/static/Feature_Importance_from_Random_Forest.png',
        'coeffic_sorted_df_json_sorted':coeffic_sorted_df_json,
        'Random_Forest_Mean_Squared_Error_txt' : Random_Forest_Mean_Squared_Error,
        'Random_Forest_R2_Score_txt' : Random_Forest_R2_Score,
        'featureimportance_txt' : featureimportance,
    }
    return render(request, 'app/data_page.html', context)

#/Users/jasonlankshear/Documents/Docker/GitHub/my_azure_app_service/static/Correlation_Matrix.png
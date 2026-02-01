"""
Train an Ordinary Least Squares (OLS) regression model on Bitcoin price data,
evaluate its performance, and generate visualizations and diagnostic plots.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from LinearRegDiagnostic import LinearRegDiagnostic
from statsmodels.regression.linear_model import OLS
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pickle
import json
from pathlib import Path


def find_project_root(marker=".gitignore"):
    """
    Find the project root directory by looking for a specific marker file.
    """
    path = Path(__file__).resolve()
    for parent in path.parents:
        if (parent / marker).exists():
            return parent
    raise FileNotFoundError(f"Project root not found with marker: {marker}")


def load_data():
    """
    Load training and testing data from CSV files.
    """
    project_root = find_project_root()
    train_path = project_root/"images/learningBase_bitcoin_forecast/tmp/learningBase/train/training_data.csv"
    test_path = project_root/"images/learningBase_bitcoin_forecast/tmp/learningBase/validation/test_data.csv"
    train_data = pd.read_csv(train_path)
    test_data = pd.read_csv(test_path)
    if 'Date' in train_data.columns:
        train_data = train_data.drop('Date', axis=1)
    if 'Date' in test_data.columns:
        test_data = test_data.drop('Date', axis=1)
    target_column = 'Close'

    # Separate features (X) and target (y)
    X_train = train_data.drop(target_column, axis=1)
    y_train = train_data[target_column]

    X_test = test_data.drop(target_column, axis=1)
    y_test = test_data[target_column]
    return X_train, y_train, X_test, y_test


def train_ols_model(X_train, y_train, X_test, y_test, target_column):
    """
    Train an OLS regression model.
    """
    feature_names = X_train.columns.tolist()
    print(f"Features used: {feature_names}")
    print(f"Target variable: {target_column}")
    X_train_const = sm.add_constant(X_train)
    X_test_const = sm.add_constant(X_test)
    print(f"\nTraining set: {X_train_const.shape[0]} samples, {X_train_const.shape[1]} features (including intercept)")
    print(f"Test set: {X_test_const.shape[0]} samples, {X_test_const.shape[1]} features (including intercept)")
    print("Training OLS model...")
    ols_model = OLS(y_train, X_train_const)
    ols_results = ols_model.fit()
    print("\n" + "="*80)
    print("MODEL SUMMARY")
    print("="*80)
    print(ols_results.summary())

    y_train_pred = ols_results.predict(X_train_const)
    y_test_pred = ols_results.predict(X_test_const)

    return y_train_pred, y_test_pred, ols_results


def evaluate_model(y_test, y_train, y_test_pred, y_train_pred):
    """
    Evaluate the model's performance using various metrics.
    """
    test_mse = mean_squared_error(y_test, y_test_pred)
    test_rmse = np.sqrt(test_mse)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    test_mape = np.mean(np.abs((y_test - y_test_pred) / y_test)) * 100

    train_mse = mean_squared_error(y_train, y_train_pred)
    train_rmse = np.sqrt(train_mse)
    train_mae = mean_absolute_error(y_train, y_train_pred)
    train_r2 = r2_score(y_train, y_train_pred)
    train_mape = np.mean(np.abs((y_train - y_train_pred) / y_train)) * 100

    print("\n" + "="*80)
    print("TRAINING SET PERFORMANCE")
    print("="*80)
    print(f"Mean Squared Error (MSE):              {train_mse:.4f}")
    print(f"Root Mean Squared Error (RMSE):        {train_rmse:.4f}")
    print(f"Mean Absolute Error (MAE):             {train_mae:.4f}")
    print(f"R-squared (R²):                        {train_r2:.4f}")
    print(f"Mean Absolute Percentage Error (MAPE): {train_mape:.2f}%")

    print("\n" + "="*80)
    print("TEST/VALIDATION SET PERFORMANCE")
    print("="*80)
    print(f"Mean Squared Error (MSE):              {test_mse:.4f}")
    print(f"Root Mean Squared Error (RMSE):        {test_rmse:.4f}")
    print(f"Mean Absolute Error (MAE):             {test_mae:.4f}")
    print(f"R-squared (R²):                        {test_r2:.4f}")
    print(f"Mean Absolute Percentage Error (MAPE): {test_mape:.2f}%")

    train_metrics = {
    'MSE': float(train_mse),
    'RMSE': float(train_rmse),
    'MAE': float(train_mae),
    'R2': float(train_r2),
    'MAPE': float(train_mape)
    }

    test_metrics = {
        'MSE': float(test_mse),
        'RMSE': float(test_rmse),
        'MAE': float(test_mae),
        'R2': float(test_r2),
        'MAPE': float(test_mape)
    }

    return train_metrics, test_metrics


def plot_visualizations(ols_results, X_train, X_test, y_train, y_test):
    """
    Generate and save visualizations including scatter plots, box plots, and diagnostic plots.
    """
    project_root = find_project_root()
    df_train = pd.concat([X_train, y_train], axis=1)
    df_test = pd.concat([X_test, y_test], axis=1)
    df = pd.concat([df_train, df_test], axis=0)

    print("Scatter plots of features vs Close Price")
    features = ['Open', 'High', 'Low', 'Volume']
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for idx, feature in enumerate(features):
        ax = axes[idx]
        
        # Scatter training
        ax.scatter(X_train[feature], y_train, color='orange', alpha=0.7, label=f'{feature} values - Training')
         
        # Scatter testing
        ax.scatter(X_test[feature], y_test, color='blue', alpha=0.7, label=f'{feature} values - Testing')
        
        # Simple regression line for this feature only
        X_single = sm.add_constant(X_train[[feature]])
        model_single = sm.OLS(y_train, X_single).fit()
        
        # Prediction line
        x_sorted = np.sort(X_train[feature])
        X_line = sm.add_constant(pd.DataFrame({feature: x_sorted}))
        y_pred_line = model_single.predict(X_line)
        
        ax.plot(x_sorted, y_pred_line, color='red', linewidth=2, label='OLS Regression Line')
        
        ax.set_xlabel(feature)
        ax.set_ylabel("Close Price")
        ax.set_title(f"{feature} vs Close Price")
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(project_root/"documentation/OLS/scatter_features.png", dpi=300, bbox_inches='tight')
    plt.close()


    print("Box Plot of all features")
    fig, ax = plt.subplots(figsize=(12, 6))
    df[['Open', 'High', 'Low', 'Close', 'Volume']].boxplot(ax=ax)
    plt.title('Box Plots of All Features - Training Set')
    plt.ylabel('Values')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(project_root/"documentation/OLS/boxplot_all_features.png", dpi=300, bbox_inches='tight')
    plt.close()

    print("Diagnostic Plots")
    diagnostic = LinearRegDiagnostic(ols_results)
    vif_table, fig, ax = diagnostic()
    fig.savefig(project_root/"documentation/OLS/diagnostic_plots.png", dpi=300, bbox_inches='tight')
    plt.close(fig)

def save_model(ols_results, feature_names, target_column, train_metrics, test_metrics):
    """
    Save the trained model, its parameters, and performance metrics to files.
    """
    project_root = find_project_root()
    # Save model (pickle format)
    with open(project_root/"documentation/OLS/currentOlsSolution.pkl", 'wb') as f:
        pickle.dump(ols_results, f)
    print("Saved: currentOlsSolution.pkl")

    with open(project_root/"documentation/OLS/currentOlsSolution.txt", 'w') as f:
        f.write("OLS MODEL PARAMETERS\n\n")
        f.write(f"Features: {', '.join(feature_names)}\n")
        f.write(f"Target: {target_column}\n\n")
        f.write("Coefficients:\n")
        for param, value in ols_results.params.items():
            f.write(f"  {param}: {value:.6f}\n")
        f.write(f"\nR-squared: {ols_results.rsquared:.6f}\n")
        f.write(f"Adjusted R-squared: {ols_results.rsquared_adj:.6f}\n")
        f.write(f"AIC: {ols_results.aic:.4f}\n")
        f.write(f"BIC: {ols_results.bic:.4f}\n")
    
    print("Saved: currentOlsSolution.txt")

    with open(project_root/"documentation/OLS/ols_performance_metrics.txt", 'w') as f:
        f.write("TRAINING METRICS:\n")
        for k, v in train_metrics.items():
            f.write(f"  {k}: {v:.4f}\n")
        f.write("\nTEST METRICS:\n")
        for k, v in test_metrics.items():
            f.write(f"  {k}: {v:.4f}\n")
    
    print("Saved: ols_performance_metrics.txt")

def main():
    """
    Main function to execute the OLS training, evaluation, and visualization.
    """
    X_train, y_train, X_test, y_test = load_data()
    target_column = 'Close'
    y_train_pred, y_test_pred, ols_results = train_ols_model(X_train, y_train, X_test, y_test, target_column)
    train_metrics, test_metrics = evaluate_model(y_test, y_train, y_test_pred, y_train_pred)
    plot_visualizations(ols_results, X_train, X_test, y_train, y_test)
    feature_names = X_train.columns.tolist()
    save_model(ols_results, feature_names, target_column, train_metrics, test_metrics)

if __name__ == "__main__":
    main()
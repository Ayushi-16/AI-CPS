import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


# paths
TRAIN_PATH = Path("/home/ayan/Downloads/AIBAS/bitcoin_price/AI-CPS/data/training_data.csv")
TEST_PATH  = Path("/home/ayan/Downloads/AIBAS/bitcoin_price/AI-CPS/data/test_data.csv")

OUT_DIR = Path("/home/ayan/Downloads/AIBAS/bitcoin_price/AI-CPS/documentation/ANN")
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH   = OUT_DIR / "ann_bitcoin_model.keras"
METRICS_PATH = OUT_DIR / "ann_performance_metrics.txt"

SEED = 123
np.random.seed(SEED)
tf.random.set_seed(SEED)


# data loading and cleaning
def load_and_clean(path):
    df = pd.read_csv(path)
    if "Date" in df.columns:
        df = df.drop(columns=["Date"])
    df = df.apply(pd.to_numeric, errors="coerce")
    df = df.dropna()
    return df

train_df = load_and_clean(TRAIN_PATH)
test_df  = load_and_clean(TEST_PATH)


TARGET = "Close"
X_cols = train_df.drop(columns=[TARGET]).columns

X_train_raw = train_df[X_cols].values
y_train_raw = train_df[[TARGET]].values

X_test_raw  = test_df[X_cols].values
y_test_raw  = test_df[[TARGET]].values


scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

X_train = scaler_X.fit_transform(X_train_raw)
X_test  = scaler_X.transform(X_test_raw)

y_train = scaler_y.fit_transform(y_train_raw).ravel()
y_test  = scaler_y.transform(y_test_raw).ravel()

# ANN model
X_tr, X_val, y_tr, y_val = train_test_split(
    X_train, y_train,
    test_size=0.2,
    shuffle=False
)
model = keras.Sequential([
    layers.Input(shape=(X_train.shape[1],)),
    layers.Dense(64, activation="relu"),
    layers.Dense(32, activation="relu"),
    layers.Dense(1)
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss="mse",
    metrics=["mae"]
)

early_stop = keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=20,
    restore_best_weights=True
)

# training
print("started training")
history = model.fit(
    X_tr, y_tr,
    validation_data=(X_val, y_val),
    epochs=200,
    batch_size=32,
    callbacks=[early_stop],
    verbose=1
)

model.save(MODEL_PATH)

# validation
print("\nstarted evaluation")
y_pred = model.predict(X_test).ravel()

mae  = mean_absolute_error(y_test, y_pred)
mse  = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2   = r2_score(y_test, y_pred)

n = len(y_test)
p = X_test.shape[1]
adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)

# saving
with open(METRICS_PATH, "w") as f:
    f.write("ANN Bitcoin Price Prediction Performance\n\n")
    f.write(f"MAE:              {mae:.6f}\n")
    f.write(f"MSE:              {mse:.6f}\n")
    f.write(f"RMSE:             {rmse:.6f}\n")
    f.write(f"R2 Score:         {r2:.6f}\n")
    f.write(f"Adjusted R2:      {adj_r2:.6f}\n")
    f.write(f"Input Features:   {p}\n")
    f.write(f"Training Epochs:  {len(history.history['loss'])}\n")

# visualization
plt.figure(figsize=(10, 5))
plt.plot(history.history["loss"], label="Train Loss (MSE)")
plt.plot(history.history["val_loss"], label="Validation Loss (MSE)")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("ANN Training vs Validation Loss")
plt.legend()
plt.tight_layout()
plt.savefig(OUT_DIR / "training_validation_curves.png")
plt.close()

residuals = y_test - y_pred
plt.figure(figsize=(8, 6))
plt.scatter(y_pred, residuals, alpha=0.5)
plt.axhline(0, linestyle="--")
plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.title("Diagnostic Plot: Residuals vs Predicted")
plt.tight_layout()
plt.savefig(OUT_DIR / "diagnostic_residuals.png")
plt.close()

plt.figure(figsize=(8, 8))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()],
         "r--")
plt.xlabel("Actual Normalized Close")
plt.ylabel("Predicted Normalized Close")
plt.title(f"ANN Prediction Accuracy (R² = {r2:.3f})")
plt.tight_layout()
plt.savefig(OUT_DIR / "prediction_scatter.png")
plt.close()

print("\nTask completed")
print(f"R2: {r2:.4f} | Adjusted R2: {adj_r2:.4f}")
print(f"Metrics saved to: {METRICS_PATH}")
print(f"Model saved to:   {MODEL_PATH}")

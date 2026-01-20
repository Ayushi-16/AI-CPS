import json
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow import keras

# Paths
TRAIN_PATH = Path("/home/ayan/Downloads/AIBAS/bitcoin_price/AI-CPS/data/training_data.csv")
TEST_PATH  = Path("/home/ayan/Downloads/AIBAS/bitcoin_price/AI-CPS/data/test_data.csv")
OUT_DIR    = Path("/home/ayan/Downloads/AIBAS/bitcoin_price/AI-CPS/documentation/ANN")
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = OUT_DIR / "currentAiSolution.keras"
SEED = 123
np.random.seed(SEED)
tf.random.set_seed(SEED)

# data load and clean
def load_and_clean(path):
    df = pd.read_csv(path)
    if 'Date' in df.columns:
        df = df.drop(columns=['Date'])
    
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna()
    return df

train_df = load_and_clean(TRAIN_PATH)
test_df  = load_and_clean(TEST_PATH)

# normalization check 
if train_df['Volume'].max() > 100:
    print("Data was not normalized. Applying Min-Max Scaling")
    scaler = MinMaxScaler()
    cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    train_df[cols] = scaler.fit_transform(train_df[cols])
    test_df[cols] = scaler.transform(test_df[cols])

# define features and target variables
target_col = "Close"
X_train = train_df.drop(columns=[target_col]).values.astype("float32")
y_train = train_df[target_col].values.astype("float32")
X_test  = test_df.drop(columns=[target_col]).values.astype("float32")
y_test  = test_df[target_col].values.astype("float32")

n_features = X_train.shape[1]

# design ANN model

model = keras.Sequential([
    keras.layers.Input(shape=(n_features,)),
    keras.layers.BatchNormalization(), 
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dense(1, activation="linear"),
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.0005), 
    loss="mse",
    metrics=["mae"],
)

# training
print("Start training.")
history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=100,
    batch_size=16,
    verbose=1,
)

model.save(MODEL_PATH)

# evaluate and visualization
y_pred = model.predict(X_test).ravel()

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))


plt.figure(figsize=(10, 5))
plt.plot(history.history["loss"], label="Train Loss (MSE)")
plt.plot(history.history["val_loss"], label="Val Loss (MSE)")
plt.title("Bitcoin ANN: Training vs Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.savefig(OUT_DIR / "curve_train_val_loss.png")
plt.close()



plt.figure(figsize=(8, 8))
plt.scatter(y_test, y_pred, alpha=0.5, color='orange')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel("Actual Normalized Price")
plt.ylabel("Predicted Normalized Price")
plt.title("ANN Prediction Accuracy")
plt.savefig(OUT_DIR / "diagnostic_scatter.png")
plt.close()

print(f"Task complete! Model saved at {MODEL_PATH}")
print(f"Test MAE Score: {mae:.3f} | RMSE: {rmse:.3f}")

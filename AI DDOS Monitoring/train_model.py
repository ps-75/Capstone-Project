import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

print("Loading Traffic Dataset...")
df = pd.read_csv('traffic_dataset.csv')

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(df)

joblib.dump(scaler, 'traffic_scaler.pkl')
print(" Building the Neural Network...")
input_dim = X_scaled.shape[1] 

inputs = Input(shape=(input_dim,))

encoded = Dense(16, activation='relu')(inputs)
encoded = Dense(8, activation='relu')(encoded) # The Bottleneck

decoded = Dense(16, activation='relu')(encoded)
outputs = Dense(input_dim, activation='linear')(decoded)

autoencoder = Model(inputs, outputs)
autoencoder.compile(optimizer='adam', loss='mse')

print("Training the Model (This should take less than 30 seconds)...")
history = autoencoder.fit(
    X_scaled, X_scaled, 
    epochs=20, 
    batch_size=32, 
    validation_split=0.1,
    verbose=1
)

autoencoder.save('autoencoder_model.h5')
print("\n Success! The AI is trained and saved as 'autoencoder_model.h5'.")
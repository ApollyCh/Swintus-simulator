import random
import numpy as np
from collections import deque
from tensorflow.keras import models, layers

import os
import tensorflow as tf


class Agent:
    REPLAY_MEMORY_SIZE = 10000
    BATCH_SIZE = 32
    DISCOUNT_FACTOR = 0.9
    EPSILON_DECAY = 0.9995
    MIN_EPSILON = 0.01
    LEARNING_RATE = 0.001

    def __init__(self, state_size, model_path=None):
        self.state_size = state_size
        self.memory = deque(maxlen=self.REPLAY_MEMORY_SIZE)
        self.epsilon = 1.0
        self.model = self.create_model()

    def create_model(self):
        model = models.Sequential()
        model.add(layers.Dense(64, activation='relu', input_shape=(self.state_size,)))
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(1, activation='linear'))
        model.compile(optimizer='adam', loss='mse')
        return model

    def process_state(self, state):
        # Pad or trim the state to fit `state_size`
        if len(state) < self.state_size:
            return np.pad(state, (0, self.state_size - len(state)), mode='constant')
        else:
            return np.array(state[:self.state_size])

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def get_action(self, state, valid_actions):
        if np.random.rand() < self.epsilon:
            return random.choice(valid_actions)

        processed_state = self.process_state(state).reshape(-1, self.state_size)
        action_values = [self.model.predict(processed_state)[0][0] for _ in valid_actions]
        best_action = valid_actions[np.argmax(action_values)]
        return best_action

    def replay(self):

        tf.keras.utils.disable_interactive_logging()
        if len(self.memory) < self.BATCH_SIZE:
            return

        minibatch = random.sample(self.memory, self.BATCH_SIZE)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            processed_next_state = self.process_state(next_state).reshape(-1, self.state_size)
            if not done:
                target += self.DISCOUNT_FACTOR * np.max(self.model.predict(processed_next_state)[0])

            processed_state = self.process_state(state).reshape(-1, self.state_size)
            target_f = self.model.predict(processed_state)
            target_f[0][0] = target

            self.model.fit(processed_state, target_f, epochs=1, verbose=None)

        if self.epsilon > self.MIN_EPSILON:
            self.epsilon *= self.EPSILON_DECAY

    def save_model(self, model_path):
        self.model.save(model_path)

    def load_model(self, model_path):
        self.model = models.load_model(model_path)

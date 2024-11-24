from deck import Deck
from player import Player
from round import Round
from agent import Agent

# Define environment and agent settings
# Initialize environment and agent settings
num_players = 2
deck = Deck()
players = [Player(f"Player {i + 1}") for i in range(num_players)]
round_instance = Round(deck, players)
state_size = len(round_instance.get_state())

# Initialize the agent
agent = Agent(state_size)
num_episodes = 1000  # Number of games to train on

# Main training loop
for episode in range(num_episodes):
    state = round_instance.reset()
    done = False
    total_rewards = [0] * num_players  # Initialize total rewards for each player

    while not done:
        valid_actions = round_instance.get_valid_actions()

        if not valid_actions:
            round_instance.draw_card_action()  # Draw card if no valid actions
            continue

        action = agent.get_action(state, valid_actions)
        next_state, reward, done = round_instance.step(action)

        # Update the total reward for the current player
        current_player_index = round_instance.current_player_idx
        total_rewards[current_player_index] += reward  # Accumulate individual reward

        # Remember experience if the agent actually made an action
        action_index = valid_actions.index(action)
        agent.remember(state, action_index, reward, next_state, done)

        # Update state for the next step
        state = next_state
        agent.replay()

    # Episode end logging
    for idx, total_reward in enumerate(total_rewards):
        print(f"Player {idx + 1} Total Reward: {total_reward}")

    # Optionally, if you still want an overall reward, you can sum total_rewards
    overall_total_reward = sum(total_rewards)
    print(f"Overall Total Reward: {overall_total_reward}")

    print(f"Episode {episode + 1}/{num_episodes} - Epsilon: {agent.epsilon:.4f}")
    with open("logs.txt", "a") as f:
        f.write(
            f"Episode {episode + 1}/{num_episodes} - Epsilon: {agent.epsilon:.4f}, Overall Total Reward: {overall_total_reward}\n")

    # Save model every 100 episodes
    if (episode + 1) % 100 == 0:
        agent.save_model(f"model_episode_{episode + 1}.h5")


import torch
from rlcard.agents import DQNAgent

from src.card import Card
from src.env import Environroment


def print_state(state, action_record):
    """Display the current state of the game."""
    print("\nPrevious Actions:")
    for player_id, action in get_previous_actions(
        state["current_player"], action_record
    ):
        print(f"  Player {player_id} chose: ", end="")
        Card.print_cards(action, wild_color=True)

    print("\nYour Hand:")
    Card.print_cards(state["hand"])

    print("\nLast Played Card:")
    Card.print_cards(state["target"], wild_color=True)

    print("\nCards Remaining for Other Players:")
    for i, num_cards in enumerate(state["num_cards"]):
        if i != state["current_player"]:
            print(f"  Player {i}: {num_cards} cards remaining.")

    print("\nAvailable Actions:")
    for idx, action in enumerate(state["legal_actions"]):
        print(f"  {idx}: ", end="")
        Card.print_cards(action, wild_color=True)
    print()


class HumanAgent:
    def __init__(self, num_actions):
        self.use_raw = True
        self.num_actions = num_actions

    @staticmethod
    def step(state):
        """Allow the human to choose an action."""
        print("\n" + "=" * 40)
        print("Your Turn!")
        print_state(state["raw_obs"], state["action_record"])
        print("=" * 40)

        while True:
            try:
                action = int(input(">> Choose an action (integer): "))
                if 0 <= action < len(state["legal_actions"]):
                    return state["raw_legal_actions"][action]
                print("Invalid choice. Please choose a valid action.")
            except ValueError:
                print("Invalid input. Enter an integer corresponding to an action.")

    def eval_step(self, state):
        """Evaluate step for the agent (same as step for humans)."""
        return self.step(state), {}


def get_previous_actions(current_player, action_record):
    """Get a list of previous actions for display."""
    return [
        record for record in reversed(action_record) if record[0] != current_player
    ][::-1]


def display_final_actions(final_state):
    """Display the final actions of the other players."""
    print("\nFinal Actions:")
    for player_id, action in get_previous_actions(
        final_state["raw_obs"]["current_player"], final_state["action_record"]
    ):
        print(f"  Player {player_id} chose: ", end="")
        Card.print_cards(action, wild_color=True)


def show_game_result(payoffs):
    """Display the game results."""
    print("\n" + "=" * 40)
    print("Game Over!")
    print("You " + "win! 🎉" if payoffs[0] > 0 else "lose! 💔")
    print("=" * 40 + "\n")


def play_again():
    """Prompt the user to play another game."""
    while True:
        replay = input("Do you want to play another game? (y/n): ").strip().lower()
        if replay in {"y", "yes"}:
            return True
        if replay in {"n", "no"}:
            return False
        print("Invalid input. Please enter 'y' or 'n'.")


def main():
    """Main game loop."""
    env = Environroment({"seed": 42, "allow_step_back": False})
    human_agent = HumanAgent(env.num_actions)
    dqn_agent = DQNAgent.from_checkpoint(
        torch.load("experiments/rlcard_dqn/checkpoint_dqn.pt")
    )
    env.set_agents([human_agent, dqn_agent])

    while True:
        print("\n" + "=" * 40)
        print("New Game Starting!")
        print("=" * 40)

        trajectories, payoffs = env.run(is_training=False)

        display_final_actions(trajectories[0][-1])
        show_game_result(payoffs)

        if not play_again():
            print("Thanks for playing! Goodbye!")
            break


if __name__ == "__main__":
    main()

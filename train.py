import argparse
import os
from datetime import datetime

import torch
from rlcard.agents import RandomAgent
from rlcard.utils import (
    Logger,
    get_device,
    plot_curve,
    reorganize,
    set_seed,
    tournament,
)

from src.env import Environroment


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="DQN/NFSP example in RLCard")
    parser.add_argument("--algorithm", type=str, default="dqn", choices=["dqn", "nfsp"])
    parser.add_argument("--cuda", type=str, default="")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_episodes", type=int, default=5000)
    parser.add_argument("--num_eval_games", type=int, default=2000)
    parser.add_argument("--evaluate_every", type=int, default=100)
    parser.add_argument(
        "--log_dir",
        type=str,
        default=f"experiments/{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}",
    )
    parser.add_argument("--load_checkpoint_path", type=str, default="")
    parser.add_argument("--save_every", type=int, default=-1)
    return parser.parse_args()


def create_agent(env, args, device):
    """Create the agent based on the algorithm and checkpoint."""
    if args.algorithm == "dqn":
        from rlcard.agents import DQNAgent

        return (
            DQNAgent.from_checkpoint(torch.load(args.load_checkpoint_path))
            if args.load_checkpoint_path
            else DQNAgent(
                num_actions=env.num_actions,
                state_shape=env.state_shape[0],
                mlp_layers=[64, 64],
                device=device,
                save_path=args.log_dir,
                save_every=args.save_every,
            )
        )
    elif args.algorithm == "nfsp":
        from rlcard.agents import NFSPAgent

        return (
            NFSPAgent.from_checkpoint(torch.load(args.load_checkpoint_path))
            if args.load_checkpoint_path
            else NFSPAgent(
                num_actions=env.num_actions,
                state_shape=env.state_shape[0],
                hidden_layers_sizes=[64, 64],
                q_mlp_layers=[64, 64],
                device=device,
                save_path=args.log_dir,
                save_every=args.save_every,
            )
        )
    else:
        raise ValueError(f"Unsupported algorithm: {args.algorithm}")


def save_model(agent, log_dir):
    """Save the trained model."""
    save_path = os.path.join(log_dir, "model.pth")
    torch.save(agent, save_path)
    print(f"Model saved in {save_path}")


def train_agent(env, args, learner):
    """Train the agent using the specified arguments and environment."""
    with Logger(args.log_dir) as logger:
        for episode in range(args.num_episodes):
            if args.algorithm == "nfsp":
                learner.sample_episode_policy()

            trajectories, payoffs = env.run(is_training=True)
            trajectories = reorganize(trajectories, payoffs)

            for ts in trajectories[0]:
                learner.feed(ts)

            if episode % args.evaluate_every == 0:
                performance = tournament(env, args.num_eval_games)[0]
                logger.log_performance(episode, performance)

        csv_path, fig_path = logger.csv_path, logger.fig_path

    plot_curve(csv_path, fig_path, args.algorithm)
    save_model(learner, args.log_dir)


def main():
    """Run the main training loop."""
    args = parse_arguments()
    os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda
    set_seed(args.seed)
    device = get_device()

    env = Environroment({"seed": args.seed, "allow_step_back": False})
    learner = create_agent(env, args, device)

    agents = [
        learner,
        *(RandomAgent(num_actions=env.num_actions) for _ in range(1, env.num_players)),
    ]

    env.set_agents(agents)
    train_agent(env, args, learner)


if __name__ == "__main__":
    main()

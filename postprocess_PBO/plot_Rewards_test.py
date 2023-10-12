import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid

def plot_rewards(rewards):
    episodes = len(rewards)
    
    avg_rewards = np.mean(rewards, axis=1)
    reward_variances = np.var(rewards, axis=1)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plot average reward
    ax.plot(range(episodes), avg_rewards, label='Average Reward', linewidth=2.5, color='tab:blue')
    
    # Plot reward variance as error bars
    ax.errorbar(range(episodes), avg_rewards, yerr=np.sqrt(reward_variances), fmt='o', markersize=4,
                color='tab:blue', ecolor='tab:blue', capsize=3, capthick=1)
    
    # Set plot properties
    ax.set_xlabel('Episode', fontsize=12)
    ax.set_ylabel('Reward', fontsize=12)
    ax.set_title('DRL Training Convergence', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10, loc='lower right')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust tick labels font size
    ax.tick_params(axis='both', which='major', labelsize=10)
    
    # Fine-tune figure layout
    fig.tight_layout()
    
    # Save the plot as a vector PDF file for high-quality output
    plt.savefig('convergence_plot.pdf', format='pdf', dpi=300)
    
    # Show the plot
    plt.show()



def plot_rewards_all(rewards):
    episodes = len(rewards)
    num_envs = len(rewards[0])
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plot individual rewards with semi-transparent lines
    for env in range(num_envs):
        env_rewards = [episode[env] for episode in rewards]
        ax.plot(range(episodes), env_rewards, alpha=0.3, color='tab:blue')
    
    # Plot average reward with solid and fully colored line
    avg_rewards = np.mean(rewards, axis=1)
    ax.plot(range(episodes), avg_rewards, label='Average Reward', linewidth=2.5, color='tab:blue')
    
    # Set plot properties
    ax.set_xlabel('Episode', fontsize=12)
    ax.set_ylabel('Reward', fontsize=12)
    ax.set_title('DRL Training Convergence', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10, loc='lower right')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust tick labels font size
    ax.tick_params(axis='both', which='major', labelsize=10)
    
    # Fine-tune figure layout
    fig.tight_layout()
    
    # Save the plot as a vector PDF file for high-quality output
    plt.savefig('convergence_plot.pdf', format='pdf', dpi=300)
    
    # Show the plot
    plt.show()




def plot_rewards_with_images(rewards, images, zoom_episodes):
    episodes = len(rewards)
    num_images = len(zoom_episodes)

    fig, (ax_reward, ax_images) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, num_images]})

    # Plot reward evolution
    ax_reward.plot(range(episodes), rewards, color='tab:blue')
    ax_reward.set_xlim(0, episodes)
    ax_reward.set_ylim(min(rewards), max(rewards))
    ax_reward.set_xlabel('Episode')
    ax_reward.set_ylabel('Reward')
    ax_reward.set_title('Reward Evolution')
    ax_reward.grid(True, linestyle='--', alpha=0.7)

    # Calculate the number of rows and columns for the image grid
    num_rows = int(np.ceil(num_images / 5))
    num_cols = min(num_images, 5)
    nrows_ncols = num_rows * 100 + num_cols

    # Create a grid of subplots for the images
    grid = ImageGrid(fig, 111, nrows_ncols=(num_rows, num_cols), axes_pad=0.5, aspect=True)

    # Plot images and marker lines
    for i, zoom_episode in enumerate(zoom_episodes):
        ax_image = grid[i]
        ax_image.imshow(images[zoom_episode], cmap='gray')
        ax_image.set_xticks([])
        ax_image.set_yticks([])

        ax_reward.axvline(x=zoom_episode, color='red', linestyle='--')
        ax_image.axvline(x=zoom_episode, color='red', linestyle='--')

    # Adjust spacing between subplots
    plt.subplots_adjust(hspace=0.5)

    # Save the figure as an image file
    plt.savefig('reward_evolution_with_images.png', dpi=300)

    # Show the figure
    plt.show()

# Example usage
rewards = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.5, 1.4, 1.3, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
images = {10: np.random.rand(100, 100), 20: np.random.rand(100, 100), 30: np.random.rand(100, 100)}
zoom_episodes = [10, 20, 30]

plot_rewards_with_images(rewards, images, zoom_episodes)
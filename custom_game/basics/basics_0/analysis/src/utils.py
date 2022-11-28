
from src.configs import *
# ============================================== #
# Setup Data
# ============================================== #

def set_seeds():
    np.random.seed(0)


def load_dataset(name="seats"):

    if name == "seats":
        with open(str(SEATS_DATASET), 'rb') as f:
            data = pickle.load(f)
        return pd.DataFrame(data=data, columns=["x_coord", "y_coord"])


# ============================================== #
# Process Data
# ============================================== #

def train_kmeans(df):
    X = df.values
    k_means = KMeans(init="k-means++", n_clusters=N_CLUSTERS, n_init=10)
    t0 = time.time()    
    k_means.fit(X)
    t_batch = time.time() - t0
    return k_means, t_batch


def assign_claster(df, k_means):
    X = df.values
    k_means_cluster_centers = k_means.cluster_centers_
    k_means_labels = pairwise_distances_argmin(X, k_means_cluster_centers)
    df["cluster"] = k_means_labels
    return df

# ============================================== #
# Plot Data
# ============================================== #

def plot_raw_data(df, show=False):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    sns.scatterplot(data=df, x="x_coord", y="y_coord", ax=ax)
    img_raw_data_path: str = str(IMAGES / Path("raw_data.png"))
    plt.savefig(img_raw_data_path)
    if show:
        plt.show()
    else:
        plt.close()

def plot_kmeans(k_means, X, t_batch, show=False):
    fig = plt.figure(figsize=(10, 10))
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)
    colors = ["#4EACC5", "#FF9C34", "#4E9A06", "#52069a", "#8F8B66"]
    colors = colors + ["#CC0605", "#D36E70", "#354D73", "#6C3B2A", "#646B63"]
    colors = colors + ["#20603D", "#C7B446"]

    colors = colors[0:N_CLUSTERS]

    k_means_cluster_centers = k_means.cluster_centers_
    k_means_labels = pairwise_distances_argmin(X, k_means_cluster_centers)

    # KMeans
    ax = fig.add_subplot(1, 1, 1)
    for k, col in zip(range(N_CLUSTERS), colors):
        my_members = k_means_labels == k
        cluster_center = k_means_cluster_centers[k]
        ax.plot(X[my_members, 0], X[my_members, 1], "w", markerfacecolor=col, marker=".")
        ax.plot(
            cluster_center[0],
            cluster_center[1],
            "o",
            markerfacecolor=col,
            markeredgecolor="k",
            markersize=6,
        )
    ax.set_title("KMeans")
    ax.set_xticks(())
    ax.set_yticks(())
    # ax.text(-3.5, 1.8, "train time: %.2fs\ninertia: %f" % (t_batch, k_means.inertia_))
    ax.text(+500, +500, "train time: %.2fs\ninertia: %f" % (t_batch, k_means.inertia_))

    img_cluster_filepath: str = str(IMAGES / Path("clusters_and_centroids.png"))
    plt.savefig(img_cluster_filepath)
    if show:
        plt.show()
    else:
        plt.close()


# ============================================== #
# Save Data
# ============================================== #

def save_clusters(df: pd.DataFrame):
    df.to_csv(str(CLUSTERS), index=False)


def save_centroids(centroids):
    np.savetxt(CENTROIDS, centroids, delimiter=',')
    pass

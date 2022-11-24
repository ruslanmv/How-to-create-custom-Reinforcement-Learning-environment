from src.libs import *
from src.configs import *
from src.utils import load_dataset, set_seeds, plot_kmeans, train_kmeans
from src.utils import assign_claster, save_clusters, save_centroids


def main():
    logger.info("Setup..")
    set_seeds()
    df = load_dataset() # print(df.head())

    """fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    sns.scatterplot(data=df, x="x_coord", y="y_coord", ax=ax)
    plt.show()"""

    logger.info("Fit...")
    k_means, t_batch = train_kmeans(df=df)
    logger.info(f"Elapsed time: {t_batch:.4f}")

    logger.info("Show results...")
    plot_kmeans(k_means=k_means, X=df.values, t_batch=t_batch)

    k_means_cluster_centers = k_means.cluster_centers_
    logger.info(k_means_cluster_centers)
    
    logger.info("Assign Clusters...")
    assign_claster(df=df, k_means=k_means)

    logger.info("Save data...")
    save_clusters(df=df)

    save_centroids(centroids=k_means_cluster_centers)

    # logger.info("Finish\n")


if __name__ == "__main__":
    main()

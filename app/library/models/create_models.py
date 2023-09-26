import multiprocessing

from sklearn.manifold import TSNE
#import umap as umapo
import numpy as np


def tsne(
        iter=5000,
        begin_p=10,
        end_p=51,
        step_p=10,
        seed=24,
        early_ex=30,
        metric='euclidean'
        ) -> dict:
    """
    Creates multiple TSNE models according to the specs of the arguments.

    Args:
    iter (int): Number of iterations.
    begin_p (int): The minumum value of the perplexities that get generated.
    end_p (int): The maximum value of the perplexities that get generated.
    step_p (int): In what increments the perplexities should be generated

    Returns:
    dict: All the generated TSNE models.
    Each key contains the perplexity value of the model.
    """
    n_threads = multiprocessing.cpu_count()
    models = {}
    
    print(f'[GENERATE][ENTER] tsne()') 
    print(f'[INFO] perplexity values: begin_p: {begin_p}, end_p: {end_p}')
    print(f'[INFO] threads: {n_threads}')

    if 'euclidean' not in metric:
        metric = 'precomputed'

    for i in range(begin_p, end_p):
        print(i)
        models['p{}'.format(i)] = {
            'model':
                TSNE(
                    metric=metric,
                    n_components=2,
                    random_state=seed,
                    n_jobs=n_threads,
                    n_iter=iter,
                    perplexity=i,
                    early_exaggeration=early_ex
                    )
                }
    print(f'[GENERATE][EXIT] tsne()')
    return models


def umap(
        n_neighbors_range=(10, 25),
        n_neighbors_step=5,
        min_dist_range=(0.05, 0.21),
        min_dist_step=0.05,
        n_neighbors=15,
        metric='euclidean',
        n_epochs=None
        ) -> dict:
    """
    Creates multiple UMAP models according to the specs of the arguments.

    Args:
    n_neighbors (int): This parameter controls how UMAP balances local versus
    global structure in the data. low is local, high is more global.

    min_dist (int): The min_dist parameter controls how tightly UMAP is
    allowed to pack points together.

    metric (str): This controls how distance is computed in the ambient space
    of the input data.


    Metric types:
    Minkowski style metrics:
        * euclidean
        * manhattan
        * chebyshev
        * minkowski

    Miscellaneous spatial metrics:

        * canberra
        * braycurtis
        * haversine

    Normalized spatial metrics:

        * mahalanobis
        * wminkowski
        * seuclidean

    Angular and correlation metrics:
        * cosine
        * correlation
    """

    models = {}
    print('umap')
    for c_neighbors in range(
            n_neighbors_range[0],
            n_neighbors_range[1],
            n_neighbors_step
            ):
        print('neighbors: {}'.format(c_neighbors))
        for c_min_dist in np.arange(
                min_dist_range[0],
                min_dist_range[1],
                min_dist_step
                ):
            c_min_dist = round(c_min_dist, 2)
            print('c_min_dist: {}'.format(c_min_dist))
            # models['n{}_d{}'.format(c_neighbors, c_min_dist)] = {
            #     'model':
            #         umapo.UMAP(
            #             n_neighbors=c_neighbors,
            #             min_dist=c_min_dist,
            #             metric=metric,
            #             n_epochs=n_epochs
            #         )
            # }
    return models

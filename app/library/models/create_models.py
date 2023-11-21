import multiprocessing

from sklearn.manifold import TSNE
import umap as umapo
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
    print(f'[INFO] perplexity value: {begin_p}')
    print(f'[INFO] TSNE iterations: {iter}')
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
        min_dist=0.1,
        n_neighbors=15,
        metric='euclidean',
        n_epochs=None
        ) -> dict:
    """
    Creates multiple UMAP models according to the specs of the arguments.

    Args:
    n_neighbors (int): This parameter controls how UMAP balances local versus
    global structure in the data. low is local, high is more global. from 5 to 50

    min_dist (int): The min_dist parameter controls how tightly UMAP is
    allowed to pack points together. from 0.05 to 0.5 

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



    models['n{}_d{}'.format(n_neighbors, min_dist)] = {
        'model':
            umapo.UMAP(
                n_neighbors=n_neighbors,
                min_dist=min_dist,
                metric=metric,
                n_epochs=n_epochs
            )
    }
    return models




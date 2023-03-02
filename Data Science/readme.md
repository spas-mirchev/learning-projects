# Data Science projects

I started building a full-stack platform for discovering early-stage musicians (i.e. Spotify for debut albums). With it, I faced the challenge of creating a good recommendation algorithm that tackles both the ‘cold-start’ problem, as well as the ‘over-recommendation’ problem. I read how companies such as Spotify and YouTube have approached those problems over the years.

I initially started using the Apriori algorithm, which is used for finding association rules.

Then, I started exploring the cosine similarity algorithms - Item CF & User CF. Then I looked to use latent factors in Collaborative Filtering.

### Data

For my experiments I used the same dataset of Artists, Users and Scrobbles from [Lastfm](https://www.kaggle.com/code/pcbreviglieri/recommending-music-artists-with-boltzmann-machines/data).

### Recommendation algorithms

1. [Apriori](recommendation_models/apriori.ipynb)
2. [Item Collaborative Filtering (CF) & User Collaborative Filtering (CF)](recommendation_models/item_to_item.ipynb)
3. [Matrix factorization](recommendation_models/collaborative_filtering.ipynb)
4. [Light GCN](recommendation_models/lightGCN.ipynb)

### Future exploration

I'd like to study graph-based recommendation systems more in-depth to see how they would compare to the current algorithms.

### Other experiments

- [Experiments](recommendation_models/experiments)

### Technologies

- Pytorch
- Numpy
- Pandas
- Plotty
- Matplot
- OpenCV

### Credits

[Kaggle Lastfm Recommending Music Artists Data](https://www.kaggle.com/code/pcbreviglieri/recommending-music-artists-with-boltzmann-machines/data).

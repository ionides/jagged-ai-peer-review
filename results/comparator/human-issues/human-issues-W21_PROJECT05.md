# Human Issues — W21 Project 05

1. There is evidence of model misspecification. The perturbed model (with parameters having a random walk) obtains log likelihoods around -300. As the perturbations decrease, the likelihood goes down and filtering failures (large drops in the estimated likelihood) start occurring. This is most likely a result of insufficient process and/or measurement noise.

2. All models use binomial measurement, which can be problematic partly because of the bounded support and partly because it cannot fit overdispersion. Similarly, no models included additional noise in the rates.

3. The model is not fully described (via mathematical equations). The parameter eta is not defined, except by the computer code.

4. Initializing to $I=1$ seems a strong assumption, but works out okay here.

5. Reference list is limited to course notes, plus the data set source. More context could be added.

6. The likelihood at the initial guess is not scientifically as important as the likelihood after parameter estimation - better to report the latter instead.

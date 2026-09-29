# Human Issues — W21 Project 08

1. The decreasing likelihood in the HMM search is likely a symptom of model misspecification: the model needs extra noise to explain the data, and this noise is provided by the perturbations in early iterations of the IF2 optimization. As the optimization algorithm decreases the perturbations, the perturbed likelihood goes down even as the proper likelihood (of the actual model, without perturbations) increases.

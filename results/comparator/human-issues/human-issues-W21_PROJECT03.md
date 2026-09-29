# Human Issues — W21 Project 03

1. The scatterplot for the SIR global search shows that some combinations of parameters are well identified (e.g., trade-off between β, ρ and μ_IR). The flat likelihood surface shows that some combinations are unidentifiable. This is not a problem with the maximization, which reliably gets within 5-10 log units of the maximum. It is just a fact that the data follow exponential decay which can be described well by 2 or 3 parameters.

2. The ordinary differential equation (ODE) models written down do not perfectly match the POMP model implemented. The ODE is a deterministic skeleton corresponding to the POMP model.

3. The first SIRV model fits considerably better (8 units of log likelihood gained, for two degrees of freedom, the parameters u and σ). The model is still not fully identifiable, but that is not needed to do a likelihood ratio test.

4. The second SIRV model does not give this improvement in log likelihood, so gives a worse description of vaccination. One could investigate why, e.g., by looking at conditional log likelihoods to see which time points are less well described. A problem with the coding of this model is that there is a t² in the model for vaccination which is incorrectly included as dt² in the latent process model equations and code. That could explain some of the issue.

5. There could be benefits from running the code for longer, perhaps even using the greatlakes cluster.

6. For the fitted models, it might be useful for interpretation to calculate and discuss the R_0 values corresponding to the fitted parameters. Here, a simple formula is R_0 = β/μ_IR which is much less than one.

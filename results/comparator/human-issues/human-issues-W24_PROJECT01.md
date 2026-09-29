# Human Issues — W24 Project 01

1. The dataset must somehow determine whether an election is free and fair, since many autocracies claim to have a democratic mandate. A brief explanation would help the reader.

2. Is there an error in Fig. 1? $Z(t)$ seems to be defined as non-negative. It is unusual to require $\Delta(Z(t))$ to be non-negative.

3. The diagram is written with $S$ as a compartment, and in the Csnippet the value of `S` changes dynamically. For a covariate, the value would be data. New sovereign states entering $S$ could be considered as a covariate process, analogous to birth/immigration in an epidemic model.

4. $\Delta Z(t)$ is described as the number of democracies, but is it actually the change in that number? Perhaps the plot of the graphs for $Z(t)$ and $\Delta Z(t)$ seem incorrectly labeled. The graph on the right looks like the differences of the $Z(t)$ values, without performing the transform defined for $\Delta Z(t)$, while the graph on the left aligns more with the newly defined $\Delta Z(t)$, the positive change of new democratic states.

5. From the measurement model, it is clear that $N$ counts democracies. But, the model does not let states return from democracy to autocracy?

6. The $P$ and $R$ components are not clearly defined. $P$ should maybe be defined as the change in the number of states that are still under the control of powerful elites who are for the current state. Then the states that are under heavy influence of the elites would then transition to state $R$, which is the change in the number of states that enter a revolution, or revolution is threatened. The way the model is defined leaves me to believe that there should be a state after $N$, which would be the final compartment for states that achieve democracy, instead of remaining in negotiations, or going back to revolution. The variables $\beta$ and $R(t)$ are introduced, and while $R(t)$ is previously defined, $\beta$ isn't given a definition, so at this point, no intuition is given as to what this variable represents.

7. In Fig. 4, $\beta$ and $\mu_{PR}$ plots would be clearer with the x-axis on a log scale.

8. Fig. 7. The "moderate evidence" has p-values well above the usual evidence requirements. It is still okay to comment on small and statistically insignificant effects, but this needs explanation.

9. Section 2.2. Fig. 2 is explained to show that the parameter estimated are well identified, but some combinations of them seem weakly identified, for example the nonlinear trade-off between $\mu_{RN}$ and $\rho$.

10. In the profile, $k$ is not identifiable as it has values across its whole range that maximize the likelihood. It is nice that the project created several profiles of different parameters.

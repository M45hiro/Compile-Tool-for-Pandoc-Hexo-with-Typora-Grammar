---
title: Typora中LateX的Pandoc渲染与重编译（二）
mathjax: true
tags: [LateX, Hexo, Pandoc, Recompile, Regex]
abstract: 本文是渲染结果。

---

<!-- more -->


Thus we can provide a posterior distribution merely dependent on the joint distribution $\\\textit{p}(\\\boldsymbol{u}_t,\boldsymbol{v}_t)$, which can be sampled easily and precisely. Next, we consider how to formulate the mapping from the joint distribution to the posterior distribution. Typically used methods are Bayesian estimation or classifier-free guidance. Inevitably, the maximum posterior estimation required for Bayesian estimation is straightly upon with the prior knowledge of different tasks, while the classifier-free guidance is related to the quality of the representation extracted from joint distribution, which fails to accurately extract features from the source images cause its high correlation with noise standard in diffusion process. Fortunately, benefit from the analytical nature of our $\\\textit{p}(\\\boldsymbol{u}_t, \boldsymbol{v}_t)$, it's possible to provide a close-form of posterior distribution. Likewise, we should employ the previously introduced neighborhood condition in this step. Firstly, according to Bayes' theorem

$$
\begin{equation}
\begin{aligned}
&\nabla_{\boldsymbol{x_t}} \log p(\boldsymbol{x}_t|\hat{\boldsymbol{u}}_t,\hat{\boldsymbol{v}}_t) \\\notag\\
&= \nabla_{\boldsymbol{x_t}} \log p(\boldsymbol{x}_t) + \nabla_{\boldsymbol{x_t}} \log p(\hat{\boldsymbol{u}}_t,\hat{\boldsymbol{v}}_t|\boldsymbol{x}_t),
\end{aligned}
\end{equation}
$$

it is worth noting that in the neighborhood $\\\Theta$, $\\\textit{x}_t, \hat{\boldsymbol{u}}_t, \hat{\boldsymbol{v}}_t$can be approximate expressed as

$$
\begin{equation}
\begin{aligned}
&\nabla_{\boldsymbol{x}_t} \log p(\hat{\boldsymbol{u}}_t, \hat{\boldsymbol{v}}_t|\boldsymbol{x}_t) \\
&=\nabla_{\boldsymbol{x}_t + \boldsymbol{\delta}} \log p(\hat{\boldsymbol{u}}_t, \hat{\boldsymbol{v}}_t|\boldsymbol{x}_t + \boldsymbol{\delta})\\\notag\\
&= \nabla_{\hat{\boldsymbol{u}}_t} \log p(\hat{\boldsymbol{u}}_t|\hat{\boldsymbol{u}}_t) + \nabla_{\hat{\boldsymbol{v}}_t} \log p(\hat{\boldsymbol{v}}_t|\hat{\boldsymbol{v}}_t)\\\notag\\
&= \nabla_{\hat{\boldsymbol{u}}_t} \log p(\hat{\boldsymbol{u}}_t) + \nabla_{\hat{\boldsymbol{v}}_t} \log p(\hat{\boldsymbol{v}}_t),
\end{aligned}
\\\label{neighbor}
\end{equation}
$$

then

$$
\begin{equation}
\begin{aligned}
&\nabla_{\boldsymbol{x_t}} \log p(\boldsymbol{x}_t|\hat{\boldsymbol{u}}_t,\hat{\boldsymbol{v}}_t) \\\notag\\
&= \nabla_{\boldsymbol{x_t}} \log p(\boldsymbol{x}_t) + \nabla_{\hat{\boldsymbol{u}}_t} \log p(\hat{\boldsymbol{u}}_t) + \nabla_{\hat{\boldsymbol{v}}_t} \log p(\hat{\boldsymbol{v}}_t).
\end{aligned}
\\\label{fsrvs}
\end{equation}
$$

Consequently, a closed-form posterior distribution can be derived, relying only on the unconditional generative distribution and the source image distributions along the forward diffusion process. The unconditional distribution is obtained via a pre-trained DDPM, whereas the source image distributions are computed directly from the forward process. 
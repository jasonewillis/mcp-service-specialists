# Statistician Agent - Technical Mastery Knowledge Base

**Version**: 1.0  
**Date**: January 19, 2025  
**Purpose**: Technical expertise for Statistician MCP agent to research and provide statistical implementation guidance  
**Usage**: Knowledge base for researching statistical methods and providing mathematical implementation prompts  

---

## 🎯 **TECHNICAL MASTERY: Statistical Analysis Implementation Expertise**

### **Probability Theory and Distributions**

#### **Probability Foundations**
```yaml
Probability Axioms and Rules:
  Kolmogorov Axioms:
    "P(A) ≥ 0 for any event A"
    "P(Ω) = 1 where Ω is the sample space"
    "P(A₁ ∪ A₂ ∪ ...) = P(A₁) + P(A₂) + ... for mutually exclusive events"
    
  Fundamental Rules:
    Addition Rule: "P(A ∪ B) = P(A) + P(B) - P(A ∩ B)"
    Multiplication Rule: "P(A ∩ B) = P(A|B) × P(B) = P(B|A) × P(A)"
    Conditional Probability: "P(A|B) = P(A ∩ B) / P(B), provided P(B) > 0"
    Law of Total Probability: "P(A) = Σ P(A|Bᵢ) × P(Bᵢ)"
    Bayes' Theorem: "P(A|B) = P(B|A) × P(A) / P(B)"

Independence and Dependence:
  Statistical Independence:
    Definition: "P(A ∩ B) = P(A) × P(B)"
    Equivalent: "P(A|B) = P(A) and P(B|A) = P(B)"
    
  Conditional Independence:
    Definition: "P(A ∩ B|C) = P(A|C) × P(B|C)"
    Applications: "Naive Bayes assumptions, Markov models"

Random Variables:
  Discrete Random Variables:
    Probability Mass Function: "P(X = x) for discrete values"
    Cumulative Distribution Function: "F(x) = P(X ≤ x)"
    Expected Value: "E[X] = Σ x × P(X = x)"
    Variance: "Var(X) = E[X²] - (E[X])²"
    
  Continuous Random Variables:
    Probability Density Function: "f(x) where P(a < X < b) = ∫ₐᵇ f(x) dx"
    Properties: "f(x) ≥ 0 and ∫₋∞^∞ f(x) dx = 1"
    Expected Value: "E[X] = ∫₋∞^∞ x f(x) dx"
    Variance: "Var(X) = ∫₋∞^∞ (x - μ)² f(x) dx"
```

#### **Common Probability Distributions**
```yaml
Discrete Distributions:
  Bernoulli Distribution:
    Parameters: "p (probability of success)"
    PMF: "P(X = 1) = p, P(X = 0) = 1-p"
    Mean: "p"
    Variance: "p(1-p)"
    Implementation: "scipy.stats.bernoulli"
    
  Binomial Distribution:
    Parameters: "n (trials), p (probability of success)"
    PMF: "P(X = k) = C(n,k) × p^k × (1-p)^(n-k)"
    Mean: "np"
    Variance: "np(1-p)"
    Implementation: "scipy.stats.binom"
    Use Cases: "Quality control, A/B testing, clinical trials"
    
  Poisson Distribution:
    Parameter: "λ (rate parameter)"
    PMF: "P(X = k) = e^(-λ) × λ^k / k!"
    Mean: "λ"
    Variance: "λ"
    Implementation: "scipy.stats.poisson"
    Use Cases: "Count data, rare events, queueing theory"
    
  Negative Binomial Distribution:
    Parameters: "r (successes), p (probability)"
    PMF: "P(X = k) = C(k+r-1, k) × p^r × (1-p)^k"
    Mean: "r(1-p)/p"
    Variance: "r(1-p)/p²"
    Implementation: "scipy.stats.nbinom"
    Use Cases: "Overdispersed count data, epidemiology"

Continuous Distributions:
  Normal Distribution:
    Parameters: "μ (mean), σ² (variance)"
    PDF: "f(x) = (1/σ√2π) × e^(-(x-μ)²/2σ²)"
    Properties: "Symmetric, bell-shaped, 68-95-99.7 rule"
    Standard Normal: "μ = 0, σ = 1, denoted as Z ~ N(0,1)"
    Implementation: "scipy.stats.norm"
    
  Student's t-Distribution:
    Parameter: "ν (degrees of freedom)"
    PDF: "Complex gamma function formula"
    Properties: "Symmetric, heavier tails than normal, approaches normal as ν → ∞"
    Use Cases: "Small sample inference, t-tests, confidence intervals"
    Implementation: "scipy.stats.t"
    
  Chi-Square Distribution:
    Parameter: "k (degrees of freedom)"
    PDF: "f(x) = (1/2^(k/2)Γ(k/2)) × x^(k/2-1) × e^(-x/2)"
    Mean: "k"
    Variance: "2k"
    Use Cases: "Goodness of fit, independence tests, variance estimation"
    Implementation: "scipy.stats.chi2"
    
  F-Distribution:
    Parameters: "d₁, d₂ (degrees of freedom)"
    PDF: "Complex beta function formula"
    Use Cases: "ANOVA, regression F-tests, variance ratio tests"
    Implementation: "scipy.stats.f"
    
  Exponential Distribution:
    Parameter: "λ (rate parameter)"
    PDF: "f(x) = λe^(-λx) for x ≥ 0"
    Mean: "1/λ"
    Variance: "1/λ²"
    Use Cases: "Survival analysis, reliability, waiting times"
    Implementation: "scipy.stats.expon"
    
  Beta Distribution:
    Parameters: "α, β (shape parameters)"
    PDF: "f(x) = x^(α-1)(1-x)^(β-1) / B(α,β) for 0 < x < 1"
    Mean: "α/(α+β)"
    Variance: "αβ/((α+β)²(α+β+1))"
    Use Cases: "Bayesian priors, proportions, rates"
    Implementation: "scipy.stats.beta"
```

### **Statistical Inference and Hypothesis Testing**

#### **Parameter Estimation**
```yaml
Point Estimation:
  Method of Moments:
    Concept: "Equate sample moments to population moments"
    Procedure: "Set sample mean = population mean, sample variance = population variance"
    Advantages: "Simple, intuitive"
    Disadvantages: "Not always efficient, may not exist"
    
  Maximum Likelihood Estimation (MLE):
    Concept: "Find parameters that maximize likelihood function"
    Likelihood Function: "L(θ) = ∏ f(xᵢ; θ)"
    Log-Likelihood: "ℓ(θ) = Σ log f(xᵢ; θ)"
    Properties: "Asymptotically unbiased, efficient, normal"
    
    Implementation Example:
      from scipy.optimize import minimize_scalar
      from scipy.stats import norm
      
      def neg_log_likelihood(params, data):
          mu, sigma = params
          return -np.sum(norm.logpdf(data, mu, sigma))
          
  Least Squares Estimation:
    Ordinary Least Squares: "Minimize Σ(yᵢ - ŷᵢ)²"
    Weighted Least Squares: "Account for heteroscedasticity"
    Generalized Least Squares: "Correlated errors"
    
    Properties:
      BLUE: "Best Linear Unbiased Estimator under Gauss-Markov assumptions"
      Assumptions: "Linear relationship, independence, homoscedasticity, normality"

Interval Estimation:
  Confidence Intervals:
    Definition: "Interval that contains true parameter with specified probability"
    Interpretation: "If we repeat sampling, α% of intervals will contain true parameter"
    
    For Mean (σ known): "x̄ ± z_{α/2} × (σ/√n)"
    For Mean (σ unknown): "x̄ ± t_{α/2,n-1} × (s/√n)"
    For Proportion: "p̂ ± z_{α/2} × √(p̂(1-p̂)/n)"
    For Variance: "((n-1)s²/χ²_{α/2,n-1}, (n-1)s²/χ²_{1-α/2,n-1})"
    
    Implementation:
      from scipy import stats
      confidence_interval = stats.t.interval(confidence, df, loc=sample_mean, scale=std_error)

Bootstrap Methods:
  Non-parametric Bootstrap:
    Procedure: "Resample with replacement, calculate statistic, repeat B times"
    Bootstrap Distribution: "Approximates sampling distribution of statistic"
    Confidence Intervals: "Percentile method, bias-corrected and accelerated (BCa)"
    
    Implementation:
      import numpy as np
      from sklearn.utils import resample
      
      bootstrap_samples = []
      for i in range(n_bootstrap):
          sample = resample(data)
          bootstrap_samples.append(statistic_function(sample))
```

#### **Hypothesis Testing Framework**
```yaml
Hypothesis Testing Components:
  Null Hypothesis (H₀): "Statement of no effect or no difference"
  Alternative Hypothesis (H₁): "What we want to establish"
  
  Types of Alternatives:
    Two-tailed: "H₁: μ ≠ μ₀"
    Upper-tailed: "H₁: μ > μ₀"
    Lower-tailed: "H₁: μ < μ₀"
    
  Test Statistic: "Function of sample data used for decision"
  P-value: "Probability of observing test statistic as extreme as observed, given H₀ is true"
  Significance Level (α): "Probability of Type I error (rejecting true H₀)"
  
  Decision Rule:
    "If p-value ≤ α, reject H₀"
    "If p-value > α, fail to reject H₀"

Error Types:
  Type I Error: "Reject H₀ when H₀ is true (false positive)"
  Type II Error: "Fail to reject H₀ when H₁ is true (false negative)"
  Power: "1 - β = P(reject H₀ | H₁ is true)"
  
  Factors Affecting Power:
    "Effect size (larger = more power)"
    "Sample size (larger = more power)"
    "Significance level (larger = more power)"
    "Population variability (smaller = more power)"

Common Test Statistics:
  One-sample t-test:
    Statistic: "t = (x̄ - μ₀) / (s/√n)"
    Distribution: "t_{n-1} under H₀"
    Assumptions: "Normal population or large sample"
    
  Two-sample t-test:
    Equal Variances: "t = (x̄₁ - x̄₂) / (s_p√(1/n₁ + 1/n₂))"
    Unequal Variances (Welch): "t = (x̄₁ - x̄₂) / √(s₁²/n₁ + s₂²/n₂)"
    Degrees of Freedom: "Satterthwaite approximation for unequal variances"
    
  Paired t-test:
    Statistic: "t = d̄ / (s_d/√n)"
    Where: "d̄ = mean of differences, s_d = standard deviation of differences"
    
  Chi-square Goodness of Fit:
    Statistic: "χ² = Σ (Observed - Expected)² / Expected"
    Distribution: "χ²_{k-1} where k = number of categories"
    
  Chi-square Test of Independence:
    Statistic: "χ² = Σ (O_{ij} - E_{ij})² / E_{ij}"
    Distribution: "χ²_{(r-1)(c-1)} where r = rows, c = columns"
```

### **Design of Experiments (DOE)**

#### **Experimental Design Principles**
```yaml
Fundamental Principles:
  Randomization:
    Purpose: "Eliminate bias, ensure validity of statistical inference"
    Types: "Simple randomization, block randomization, stratified randomization"
    Implementation: "Random assignment of treatments to experimental units"
    
  Replication:
    Purpose: "Estimate experimental error, increase precision"
    Types: "True replication vs pseudoreplication"
    Benefits: "Increased power, better error estimation"
    
  Blocking:
    Purpose: "Control for known sources of variation"
    Principle: "Group similar experimental units together"
    Benefits: "Reduced experimental error, increased precision"

Experimental Units vs Observational Units:
  Experimental Unit: "Smallest unit to which treatment is independently applied"
  Observational Unit: "Unit on which response is measured"
  Pseudoreplication: "Treating observational units as if they were experimental units"

Control and Treatment Structure:
  Control Groups:
    Negative Control: "No treatment"
    Positive Control: "Known effective treatment"
    Placebo Control: "Inactive treatment to control for psychological effects"
    
  Treatment Factors:
    Fixed Effects: "Treatments chosen by experimenter"
    Random Effects: "Treatments randomly sampled from population"
    Mixed Effects: "Combination of fixed and random effects"
```

#### **Common Experimental Designs**
```yaml
Completely Randomized Design (CRD):
  Structure: "Treatments assigned completely at random to experimental units"
  Model: "y_{ij} = μ + τ_i + ε_{ij}"
  Advantages: "Simple, flexible, maximum degrees of freedom for error"
  Disadvantages: "No control for extraneous variation"
  
  Analysis:
    One-way ANOVA: "Test H₀: τ₁ = τ₂ = ... = τ_t = 0"
    F-statistic: "F = MST/MSE ~ F_{t-1, t(n-1)}"
    
  Implementation:
    from scipy import stats
    f_stat, p_value = stats.f_oneway(group1, group2, group3, ...)

Randomized Complete Block Design (RCBD):
  Structure: "Each block contains all treatments, randomized within blocks"
  Model: "y_{ij} = μ + τ_i + β_j + ε_{ij}"
  Advantages: "Controls for block effects, increased precision"
  
  Analysis:
    Two-way ANOVA: "Test effects of treatments and blocks"
    Efficiency: "Compare to CRD using relative efficiency"
    
  Implementation:
    import statsmodels.api as sm
    from statsmodels.formula.api import ols
    
    model = ols('response ~ C(treatment) + C(block)', data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

Latin Square Design:
  Structure: "Two blocking factors, each treatment appears once in each row and column"
  Model: "y_{ijk} = μ + τ_i + ρ_j + γ_k + ε_{ijk}"
  Restrictions: "Number of treatments = number of rows = number of columns"
  
  Advantages: "Controls for two sources of variation"
  Disadvantages: "Restrictive, assumes no interactions"

Factorial Designs:
  2^k Design:
    Structure: "k factors, each at 2 levels"
    Treatments: "2^k treatment combinations"
    Effects: "Main effects and interactions"
    
  Main Effects:
    Factor A: "A = (sum of responses at high level - sum at low level) / (n × 2^{k-1})"
    
  Interaction Effects:
    AB Interaction: "AB = (sum of responses where A and B have same sign - sum where different sign) / (n × 2^{k-1})"
    
  Fractional Factorial:
    Purpose: "Reduce number of runs while maintaining information on important effects"
    Resolution: "Ability to estimate effects free of aliasing with lower-order effects"
    
Response Surface Methodology (RSM):
  Purpose: "Optimize response by finding optimal factor settings"
  Central Composite Design: "Factorial points + axial points + center points"
  Box-Behnken Design: "Three-level design, no axial points"
  
  Model: "y = β₀ + Σβᵢxᵢ + Σβᵢᵢxᵢ² + ΣΣβᵢⱼxᵢxⱼ + ε"
  Analysis: "Canonical analysis to find stationary point"
```

### **Regression Analysis Mastery**

#### **Simple Linear Regression**
```yaml
Model Specification:
  Population Model: "Y = β₀ + β₁X + ε"
  Assumptions: "ε ~ N(0, σ²), independence, linearity, homoscedasticity"
  
Parameter Estimation:
  Least Squares Estimators:
    Slope: "β̂₁ = Σ(xᵢ - x̄)(yᵢ - ȳ) / Σ(xᵢ - x̄)²"
    Intercept: "β̂₀ = ȳ - β̂₁x̄"
    
  Properties:
    Unbiased: "E[β̂₀] = β₀, E[β̂₁] = β₁"
    Minimum Variance: "BLUE under Gauss-Markov assumptions"
    
Inference:
  Standard Errors:
    SE(β̂₁): "σ̂√(1/Σ(xᵢ - x̄)²)"
    SE(β̂₀): "σ̂√(1/n + x̄²/Σ(xᵢ - x̄)²)"
    
  Hypothesis Tests:
    t-test for slope: "t = β̂₁ / SE(β̂₁) ~ t_{n-2}"
    F-test for regression: "F = MSR/MSE ~ F_{1,n-2}"
    
  Confidence and Prediction Intervals:
    CI for mean response: "ŷ ± t_{α/2,n-2} × SE(ŷ)"
    PI for individual response: "ŷ ± t_{α/2,n-2} × √(MSE + SE²(ŷ))"

Model Diagnostics:
  Residual Analysis:
    Residuals: "eᵢ = yᵢ - ŷᵢ"
    Standardized residuals: "rᵢ = eᵢ / √MSE"
    Studentized residuals: "tᵢ = eᵢ / (s√(1 - hᵢᵢ))"
    
  Assumption Checking:
    Linearity: "Residuals vs fitted values plot"
    Normality: "Q-Q plot, Shapiro-Wilk test"
    Homoscedasticity: "Residuals vs fitted, Breusch-Pagan test"
    Independence: "Residuals vs time order, Durbin-Watson test"
```

#### **Multiple Linear Regression**
```yaml
Model Specification:
  Matrix Form: "Y = Xβ + ε"
  Where: "Y is n×1, X is n×(p+1), β is (p+1)×1, ε is n×1"
  
Parameter Estimation:
  Normal Equations: "(X'X)β̂ = X'Y"
  Least Squares Solution: "β̂ = (X'X)⁻¹X'Y"
  Fitted Values: "Ŷ = Xβ̂ = X(X'X)⁻¹X'Y = HY"
  Hat Matrix: "H = X(X'X)⁻¹X'"
  
Inference:
  Variance-Covariance Matrix: "Var(β̂) = σ²(X'X)⁻¹"
  Standard Errors: "SE(β̂ⱼ) = σ̂√((X'X)⁻¹)ⱼⱼ"
  
  t-tests for Individual Coefficients:
    Test: "H₀: βⱼ = 0 vs H₁: βⱼ ≠ 0"
    Statistic: "t = β̂ⱼ / SE(β̂ⱼ) ~ t_{n-p-1}"
    
  F-test for Overall Regression:
    Test: "H₀: β₁ = β₂ = ... = βₚ = 0"
    Statistic: "F = MSR/MSE = (SSR/p)/(SSE/(n-p-1)) ~ F_{p,n-p-1}"

Model Selection:
  Criteria:
    R²: "Proportion of variance explained"
    Adjusted R²: "R²ₐ = 1 - (1-R²)(n-1)/(n-p-1)"
    AIC: "Akaike Information Criterion = n ln(SSE/n) + 2p"
    BIC: "Bayesian Information Criterion = n ln(SSE/n) + p ln(n)"
    
  Selection Methods:
    Forward Selection: "Start empty, add variables based on significance"
    Backward Elimination: "Start full, remove variables based on significance"
    Stepwise: "Combination of forward and backward"
    All Subsets: "Consider all possible models"

Multicollinearity:
  Detection:
    Correlation Matrix: "High pairwise correlations (|r| > 0.8)"
    Variance Inflation Factor: "VIF = 1/(1-R²ⱼ) where R²ⱼ is R² from regressing xⱼ on other predictors"
    Condition Number: "κ = √(λₘₐₓ/λₘᵢₙ) where λ are eigenvalues of X'X"
    
  Remedies:
    Ridge Regression: "Add penalty λΣβⱼ² to minimize"
    Principal Components Regression: "Use principal components as predictors"
    Variable Selection: "Remove redundant variables"
```

#### **Logistic Regression**
```yaml
Model Specification:
  Logit Link: "logit(π) = log(π/(1-π)) = β₀ + β₁x₁ + ... + βₚxₚ"
  Probability: "π = exp(β₀ + β₁x₁ + ... + βₚxₚ) / (1 + exp(β₀ + β₁x₁ + ... + βₚxₚ))"
  
Maximum Likelihood Estimation:
  Likelihood: "L(β) = ∏ πᵢʸⁱ(1-πᵢ)¹⁻ʸⁱ"
  Log-likelihood: "ℓ(β) = Σ[yᵢ log(πᵢ) + (1-yᵢ) log(1-πᵢ)]"
  Score Equations: "∂ℓ/∂β = X'(Y - π) = 0"
  
Inference:
  Wald Tests:
    Statistic: "z = β̂ⱼ / SE(β̂ⱼ) ~ N(0,1) for large samples"
    Confidence Interval: "β̂ⱼ ± z_{α/2} × SE(β̂ⱼ)"
    
  Likelihood Ratio Tests:
    Statistic: "G² = -2 log(L₀/L₁) = -2[ℓ(β̂₀) - ℓ(β̂₁)] ~ χ²_{df}"
    Where: "df = difference in number of parameters"
    
Interpretation:
  Odds Ratio: "OR = exp(βⱼ)"
  Interpretation: "For one unit increase in xⱼ, odds multiply by exp(βⱼ)"
  
Model Diagnostics:
  Deviance: "D = -2ℓ(β̂)"
  Hosmer-Lemeshow Test: "Goodness of fit test"
  ROC Curve: "Receiver Operating Characteristic"
  C-statistic: "Area under ROC curve"
  
Implementation:
  import statsmodels.api as sm
  from sklearn.linear_model import LogisticRegression
  
  # Statsmodels approach
  model = sm.Logit(y, X).fit()
  
  # Sklearn approach
  model = LogisticRegression().fit(X, y)
```

### **Analysis of Variance (ANOVA)**

#### **One-Way ANOVA**
```yaml
Model and Assumptions:
  Model: "yᵢⱼ = μ + τᵢ + εᵢⱼ"
  Where: "μ = overall mean, τᵢ = treatment effect, εᵢⱼ ~ N(0, σ²)"
  
  Assumptions:
    Independence: "Observations within and between groups are independent"
    Normality: "Errors are normally distributed"
    Homogeneity: "Equal variances across groups (homoscedasticity)"
    
Hypothesis Testing:
  Hypotheses: "H₀: μ₁ = μ₂ = ... = μₖ vs H₁: Not all means are equal"
  Equivalent: "H₀: τ₁ = τ₂ = ... = τₖ = 0"
  
ANOVA Table:
  Source | SS | df | MS | F
  Treatment | SST | k-1 | MST = SST/(k-1) | F = MST/MSE
  Error | SSE | n-k | MSE = SSE/(n-k) |
  Total | SSTO | n-1 | |
  
  Where:
    SST: "Σnᵢ(x̄ᵢ - x̄..)²"
    SSE: "ΣΣ(xᵢⱼ - x̄ᵢ)²"
    SSTO: "ΣΣ(xᵢⱼ - x̄..)²"
    
F-test:
  Test Statistic: "F = MST/MSE ~ F_{k-1, n-k} under H₀"
  Decision: "Reject H₀ if F > F_{α, k-1, n-k}"

Multiple Comparisons:
  Family-wise Error Rate: "Probability of making at least one Type I error"
  
  Bonferroni Correction:
    Adjusted α: "α' = α/m where m = number of comparisons"
    Conservative but widely applicable
    
  Tukey's HSD (Honestly Significant Difference):
    For pairwise comparisons: "HSD = q_{α,k,n-k} × √(MSE/n)"
    Where: "q is studentized range statistic"
    Controls family-wise error rate exactly
    
  Scheffe's Method:
    Most conservative: "Works for any contrast"
    Critical value: "√((k-1)F_{α,k-1,n-k})"
    
  Dunnett's Test:
    Comparing treatments to control: "Uses special tables"
    More powerful than Bonferroni for this specific case
```

#### **Two-Way ANOVA**
```yaml
Model Specifications:
  Additive Model: "yᵢⱼₖ = μ + αᵢ + βⱼ + εᵢⱼₖ"
  Interaction Model: "yᵢⱼₖ = μ + αᵢ + βⱼ + (αβ)ᵢⱼ + εᵢⱼₖ"
  
  Where:
    αᵢ: "Effect of factor A at level i"
    βⱼ: "Effect of factor B at level j"
    (αβ)ᵢⱼ: "Interaction effect between A and B"

Hypothesis Tests:
  Main Effect A: "H₀: α₁ = α₂ = ... = αₐ = 0"
  Main Effect B: "H₀: β₁ = β₂ = ... = βᵦ = 0"
  Interaction: "H₀: (αβ)ᵢⱼ = 0 for all i,j"

ANOVA Table (with interaction):
  Source | SS | df | MS | F
  A | SSA | a-1 | MSA | MSA/MSE
  B | SSB | b-1 | MSB | MSB/MSE
  A×B | SSAB | (a-1)(b-1) | MSAB | MSAB/MSE
  Error | SSE | ab(n-1) | MSE |
  Total | SSTO | abn-1 | |

Interaction Interpretation:
  No Interaction: "Effects of factors are additive"
  Significant Interaction: "Effect of one factor depends on level of other factor"
  
  Simple Effects Analysis:
    Test effect of A at each level of B
    Test effect of B at each level of A
    Use MSE from full model for error term

Fixed vs Random Effects:
  Fixed Effects: "Factor levels chosen by experimenter"
  Random Effects: "Factor levels randomly sampled from population"
  Mixed Model: "Some factors fixed, some random"
  
  Random Effects Model:
    Different F-tests: "Use appropriate error terms"
    Variance Components: "Estimate variability due to each factor"
```

### **Survey Sampling and Design**

#### **Sampling Theory Foundations**
```yaml
Basic Sampling Concepts:
  Population: "Complete set of units of interest"
  Sampling Frame: "List of units from which sample is selected"
  Sample: "Subset of population selected for study"
  Sampling Unit: "Basic unit selected in sampling process"
  
Coverage and Non-coverage:
  Coverage Error: "Difference between target population and sampling frame"
  Under-coverage: "Frame excludes some target population units"
  Over-coverage: "Frame includes non-target population units"
  
Probability Sampling:
  Definition: "Each unit has known, non-zero probability of selection"
  Advantages: "Unbiased estimation, measurable precision"
  Selection Probability: "πᵢ = P(unit i is selected)"
  
Non-probability Sampling:
  Convenience Sampling: "Select easily accessible units"
  Purposive Sampling: "Select units based on judgment"
  Quota Sampling: "Select specified number from each stratum"
  Limitations: "Potential bias, unmeasurable precision"
```

#### **Simple Random Sampling (SRS)**
```yaml
Without Replacement (WOR):
  Selection: "Each unit has equal probability n/N of selection"
  Sample Mean: "ȳ = Σyᵢ/n"
  Population Total Estimation: "T̂ = Nȳ"
  
Variance Estimation:
  Population Mean: "Var(ȳ) = (1 - n/N) × S²/n"
  Population Total: "Var(T̂) = N²(1 - n/N) × S²/n"
  
  Where S²: "S² = Σ(yᵢ - Ȳ)²/(N-1)"
  
Finite Population Correction:
  FPC: "(1 - n/N) = (N - n)/N"
  Applied when: "Sampling fraction n/N > 0.05"
  Effect: "Reduces variance when sample is large relative to population"

Sample Size Determination:
  For Estimating Mean:
    Desired Margin of Error: "d = z_{α/2} × √(Var(ȳ))"
    Required Sample Size: "n = z²_{α/2} × S² / (d² + z²_{α/2} × S²/N)"
    
  For Estimating Proportion:
    Conservative Approach: "n = z²_{α/2} × 0.25 / d²"
    With Prior Estimate: "n = z²_{α/2} × p(1-p) / d²"

Implementation:
  import numpy as np
  from scipy import stats
  
  def srs_estimate(sample, N):
      n = len(sample)
      y_bar = np.mean(sample)
      s_squared = np.var(sample, ddof=1)
      
      # Population mean estimate
      mu_hat = y_bar
      
      # Variance of mean estimate
      fpc = (N - n) / N if n/N > 0.05 else 1
      var_mu_hat = fpc * s_squared / n
      
      return mu_hat, var_mu_hat
```

#### **Stratified Sampling**
```yaml
Design Structure:
  Population Division: "Divide population into L strata"
  Within-stratum Sampling: "Select sample from each stratum"
  Stratum Sample Size: "nₕ units from stratum h"
  
Allocation Methods:
  Proportional Allocation:
    Formula: "nₕ = n × (Nₘ/N)"
    Properties: "Self-weighting, simple analysis"
    
  Optimal Allocation:
    Formula: "nₕ = n × (NₕSₕ/Σ(NₕSₕ))"
    Objective: "Minimize variance of overall estimate"
    Requires: "Prior knowledge of stratum variances"
    
  Neyman Allocation:
    Formula: "nₕ = n × (NₕSₕ/Σ(NₕSₕ))"
    Same as optimal allocation
    
Estimation:
  Stratified Mean:
    ȳₛₜ = Σ(Nₕ/N) × ȳₕ = Σ Wₕ × ȳₕ
    Where Wₕ = Nₕ/N (stratum weight)
    
  Variance:
    Var(ȳₛₜ) = Σ Wₕ² × (1 - nₕ/Nₕ) × Sₕ²/nₕ
    
Advantages:
  Precision: "Usually more precise than SRS"
  Subpopulation Analysis: "Direct estimates for strata"
  Administrative Convenience: "Separate sampling operations"
  
Design Effect:
  Definition: "Ratio of actual variance to SRS variance"
  DEFF = Var(ȳₛₜ) / Var(ȳₛᵣₛ)
  Values < 1 indicate stratification benefit
```

#### **Cluster Sampling**
```yaml
Design Structure:
  Primary Sampling Units: "Clusters (e.g., schools, households)"
  Secondary Sampling Units: "Elements within clusters (e.g., students, individuals)"
  
One-stage Cluster Sampling:
  Selection: "Select clusters, include all elements within selected clusters"
  Estimate: "ȳc = Σ(Mᵢȳᵢ)/Σ Mᵢ"
  Where: "Mᵢ = number of elements in cluster i, ȳᵢ = cluster mean"
  
Two-stage Cluster Sampling:
  Stage 1: "Select primary clusters"
  Stage 2: "Select secondary units within selected clusters"
  
  Estimation:
    Cluster Total: "tᵢ = mᵢȳᵢ" where mᵢ = sample size in cluster i
    Overall Estimate: "ȳ = Σtᵢ/Σmᵢ"
    
Intracluster Correlation:
  Definition: "ρ = Correlation between elements within same cluster"
  Effect: "ρ > 0 increases variance (elements similar within clusters)"
  Design Effect: "DEFF ≈ 1 + (m̄ - 1)ρ" where m̄ = average cluster size
  
Variance Estimation:
  Between-cluster Component: "Reflects cluster-to-cluster variation"
  Within-cluster Component: "Reflects element-to-element variation within clusters"
  
  Combined Variance:
    V(ȳc) = (1 - n/N) × S²bc/n + (1/n) × Σ(1 - mᵢ/Mᵢ) × S²wc,i/mᵢ
    
Advantages and Disadvantages:
  Advantages: "Cost efficiency, administrative convenience"
  Disadvantages: "Usually less precise than SRS, requires variance inflation"
```

---

## 🎯 **Agent Implementation Guidance**

### **How This Technical Mastery Enhances Agent Performance**

#### **Statistical Research and Implementation Support**
- **Mathematical Foundation**: Deep understanding of statistical theory and mathematical principles
- **Method Selection**: Expert knowledge of when to apply specific statistical techniques
- **Implementation Guidance**: Comprehensive code examples and parameter specifications
- **Diagnostic Expertise**: Advanced knowledge of assumption checking and model validation

#### **Problem-Solving Approach**
- **Statistical Reasoning**: Ability to identify appropriate statistical methods for research questions
- **Experimental Design**: Expert knowledge of designing studies and experiments
- **Data Analysis**: Comprehensive understanding of analysis techniques and interpretation
- **Quality Assurance**: Expertise in validation, diagnostics, and robustness checking

### **Agent Usage Instructions**

#### **When to Apply This Technical Knowledge**
```python
# Example usage in agent decision-making
if research_question.type == "hypothesis_testing":
    determine_appropriate_test()
    check_assumptions_and_requirements()
    provide_implementation_guidance()
    
if study_design.type == "experimental":
    recommend_experimental_design()
    calculate_sample_size_requirements()
    suggest_randomization_strategy()
    
if data_characteristics.has_multiple_groups:
    recommend_anova_approach()
    suggest_multiple_comparison_procedures()
    provide_effect_size_calculations()
```

#### **Research Output Enhancement**
All Statistician agent research should include:
- **Mathematical foundations** with formulas and theoretical basis
- **Assumption checking procedures** with diagnostic tests and validation methods
- **Implementation code** with specific parameters and statistical software usage
- **Interpretation guidelines** with effect sizes and practical significance
- **Alternative approaches** when assumptions are violated or methods are inappropriate

---

*This technical mastery knowledge base transforms the Statistician Agent from general guidance to deep statistical expertise, enabling sophisticated research and implementation recommendations for statistical analysis, experimental design, and mathematical modeling challenges.*

**© 2025 Fed Job Advisor - Statistician Agent Technical Mastery Enhancement**
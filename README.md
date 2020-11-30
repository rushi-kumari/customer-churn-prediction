# Customer-churn-prediction


### PROBLEM STATEMENT 

"A Bank wants to take care of it’s customer retention for its product."
The bank wants to identify customers likely to churn balances below the minimum balance.

### DATA

The dataset which can be cleanly divided in 3 categories:

Demographic information about customers:
* customer_id 

* vintage

* age 

* gender

* dependents

* occupation

* city 

Customer Bank Relationship:
customer_nw_category 

* branch_code

* days_since_last_transaction 

Transactional Information :
current_balance 

* previous_month_end_balance

* average_monthly_balance_prevQ

* average_monthly_balance_prevQ2 

* current_month_credit 

* previous_month_credit 

* current_month_debit 

* previous_month_debit 

* current_month_balance 

* previous_month_balance 

Target Variable
* churn - Average balance of customer falls below minimum balance in the next quarter (1/0)


### LIFE CYCLE OF PROJECT 
---
1. Loading Packages and Data

2. Missing Value Imputation using mode value

3. Preprocessing of data (dummy with mutiple categories to keep data strictly numeric)

4. Normalize data using standardscalar to avoid outilers

5. Model building (logistic Regression and Random Forest)

6. Evauation metrics (f1_score - weighted average of precision and recall and roc_auc_score for logistic Regression)

7. Metrics roc_auc_score for Random Forest

### CONCLUSION 

```
 The random forest model gave the best result for each fold
which was 99% in agreement with the demand of the actual business model
```
# Financial App
---

## Description
This is a financial app whose objective is to help users understand the finacial circumstances of a company that subit their financial statements to the Superintendency of Companies, Securities, and Insurance (SCVS). It should be able to produce automated reports.

The information submited to this government institution is quite complete and contains all the yearly information of the Income Statements, Balance Sheets, and Statement of Cash Flows belonging to the companies in Ecuador. There is a problem though, this information is highly imperfect; particularly the aggregated accounts such as: Total Assets, Current Liabilities, Total Equity, etc.

The project consists of two phases: The first one is the processing and standardization of all the accounts, according to the IFRS Instructive provided by the SCVS. This details which accounts are made of which, and allow for accurate calculation of the aggregated accounts. The second one is the utilization of this information to generate automated informative reports, for each of the companies based on the information submitted to the SCVS. We make use of the universal format, labels, and IDs that the SCVS requires to automate this report generation and to be able to make insightful visualizations of the information publicly available.
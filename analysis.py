"""
Healthcare Data Analysis Project
Analyzing patient treatment outcomes, costs, and resource utilization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json

# Set style for better-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ==================== STEP 1: LOAD & EXPLORE DATA ====================
print("=" * 60)
print("HEALTHCARE DATA ANALYSIS PROJECT")
print("=" * 60)

# Load the dataset
df = pd.read_csv('healthcare_data.csv')

print("\n📊 Dataset Overview:")
print(f"Total Patients: {len(df)}")
print(f"Date Range: {df['admission_date'].min()} to {df['discharge_date'].max()}")
print(f"\nColumns: {', '.join(df.columns)}")

# Basic statistics
print("\n" + "=" * 60)
print("BASIC STATISTICS")
print("=" * 60)
print(df.describe())

# Check for missing values
print("\n🔍 Missing Values:")
print(df.isnull().sum())

# ==================== STEP 2: DATA CLEANING ====================
print("\n" + "=" * 60)
print("DATA CLEANING")
print("=" * 60)

# Convert dates to datetime
df['admission_date'] = pd.to_datetime(df['admission_date'])
df['discharge_date'] = pd.to_datetime(df['discharge_date'])

# Extract month for trend analysis
df['admission_month'] = df['admission_date'].dt.to_period('M')

# Binary encoding for success
df['success_binary'] = df['treatment_success'].map({'Yes': 1, 'No': 0})
df['readmitted_binary'] = df['readmitted'].map({'Yes': 1, 'No': 0})

print("✅ Data cleaned and prepared!")
print(f"Date columns converted to datetime format")
print(f"Added binary columns for statistical analysis")

# ==================== STEP 3: KEY METRICS ANALYSIS ====================
print("\n" + "=" * 60)
print("KEY PERFORMANCE INDICATORS")
print("=" * 60)

# Overall metrics
total_patients = len(df)
avg_length_stay = df['length_of_stay'].mean()
avg_cost = df['total_cost'].mean()
success_rate = (df['success_binary'].sum() / total_patients) * 100
readmission_rate = (df['readmitted_binary'].sum() / total_patients) * 100

print(f"\n📈 Hospital Performance:")
print(f"   • Total Patients Treated: {total_patients}")
print(f"   • Average Length of Stay: {avg_length_stay:.1f} days")
print(f"   • Average Treatment Cost: ${avg_cost:,.2f}")
print(f"   • Treatment Success Rate: {success_rate:.1f}%")
print(f"   • Readmission Rate: {readmission_rate:.1f}%")

# ==================== STEP 4: CONDITION ANALYSIS ====================
print("\n" + "=" * 60)
print("ANALYSIS BY MEDICAL CONDITION")
print("=" * 60)

condition_stats = df.groupby('condition').agg({
    'patient_id': 'count',
    'length_of_stay': 'mean',
    'total_cost': 'mean',
    'success_binary': 'mean',
    'readmitted_binary': 'mean'
}).round(2)

condition_stats.columns = ['Patient_Count', 'Avg_Stay_Days', 'Avg_Cost', 'Success_Rate', 'Readmission_Rate']
condition_stats['Success_Rate'] = (condition_stats['Success_Rate'] * 100).round(1)
condition_stats['Readmission_Rate'] = (condition_stats['Readmission_Rate'] * 100).round(1)

print("\n", condition_stats)

# Find best and worst performing conditions
best_condition = condition_stats['Success_Rate'].idxmax()
worst_condition = condition_stats['Success_Rate'].idxmin()
most_expensive = condition_stats['Avg_Cost'].idxmax()

print(f"\n🏆 Key Findings:")
print(f"   • Best Success Rate: {best_condition} ({condition_stats.loc[best_condition, 'Success_Rate']:.1f}%)")
print(f"   • Needs Improvement: {worst_condition} ({condition_stats.loc[worst_condition, 'Success_Rate']:.1f}%)")
print(f"   • Most Expensive: {most_expensive} (${condition_stats.loc[most_expensive, 'Avg_Cost']:,.2f})")

# ==================== STEP 5: TREATMENT TYPE ANALYSIS ====================
print("\n" + "=" * 60)
print("TREATMENT TYPE EFFECTIVENESS")
print("=" * 60)

treatment_stats = df.groupby('treatment_type').agg({
    'patient_id': 'count',
    'total_cost': 'mean',
    'success_binary': 'mean',
    'length_of_stay': 'mean'
}).round(2)

treatment_stats.columns = ['Patient_Count', 'Avg_Cost', 'Success_Rate', 'Avg_Stay']
treatment_stats['Success_Rate'] = (treatment_stats['Success_Rate'] * 100).round(1)

print("\n", treatment_stats)

# ==================== STEP 6: AGE ANALYSIS ====================
print("\n" + "=" * 60)
print("AGE GROUP ANALYSIS")
print("=" * 60)

# Create age groups
df['age_group'] = pd.cut(df['age'], bins=[0, 35, 50, 65, 100], 
                         labels=['Young (18-35)', 'Middle (36-50)', 'Senior (51-65)', 'Elderly (66+)'])

age_analysis = df.groupby('age_group').agg({
    'patient_id': 'count',
    'total_cost': 'mean',
    'length_of_stay': 'mean',
    'success_binary': 'mean'
}).round(2)

age_analysis.columns = ['Patient_Count', 'Avg_Cost', 'Avg_Stay', 'Success_Rate']
age_analysis['Success_Rate'] = (age_analysis['Success_Rate'] * 100).round(1)

print("\n", age_analysis)

# Correlation between age and cost
age_cost_corr = df['age'].corr(df['total_cost'])
print(f"\n📊 Age-Cost Correlation: {age_cost_corr:.3f}")
if age_cost_corr > 0.3:
    print("   → Moderate positive correlation: Older patients tend to have higher costs")

# ==================== STEP 7: INSURANCE ANALYSIS ====================
print("\n" + "=" * 60)
print("INSURANCE TYPE ANALYSIS")
print("=" * 60)

insurance_stats = df.groupby('insurance_type').agg({
    'patient_id': 'count',
    'total_cost': 'mean',
    'length_of_stay': 'mean'
}).round(2)

insurance_stats.columns = ['Patient_Count', 'Avg_Cost', 'Avg_Stay']
print("\n", insurance_stats)

# ==================== STEP 8: MONTHLY TRENDS ====================
print("\n" + "=" * 60)
print("MONTHLY ADMISSION TRENDS")
print("=" * 60)

monthly_trends = df.groupby('admission_month').agg({
    'patient_id': 'count',
    'total_cost': 'mean'
}).round(2)

monthly_trends.columns = ['Admissions', 'Avg_Cost']
print("\n", monthly_trends)

# ==================== STEP 9: COST OPTIMIZATION INSIGHTS ====================
print("\n" + "=" * 60)
print("COST OPTIMIZATION OPPORTUNITIES")
print("=" * 60)

# Find expensive conditions with long stays
expensive_long_stay = df[(df['total_cost'] > df['total_cost'].median()) & 
                         (df['length_of_stay'] > df['length_of_stay'].median())]

print(f"\n💰 High-Cost, Long-Stay Cases: {len(expensive_long_stay)} patients")
print(f"   Average Cost: ${expensive_long_stay['total_cost'].mean():,.2f}")
print(f"   Average Stay: {expensive_long_stay['length_of_stay'].mean():.1f} days")
print(f"   Top Conditions: {expensive_long_stay['condition'].value_counts().head(3).to_dict()}")

# ==================== STEP 10: STATISTICAL INSIGHTS ====================
print("\n" + "=" * 60)
print("STATISTICAL CORRELATIONS")
print("=" * 60)

# Correlation matrix
correlations = df[['age', 'length_of_stay', 'total_cost', 'doctor_visits', 'success_binary']].corr()
print("\n", correlations.round(3))

print("\n🔍 Key Correlations:")
print(f"   • Length of Stay ↔ Cost: {correlations.loc['length_of_stay', 'total_cost']:.3f}")
print(f"   • Age ↔ Length of Stay: {correlations.loc['age', 'length_of_stay']:.3f}")
print(f"   • Doctor Visits ↔ Cost: {correlations.loc['doctor_visits', 'total_cost']:.3f}")

# ==================== STEP 11: SAVE RESULTS FOR DASHBOARD ====================
print("\n" + "=" * 60)
print("GENERATING DASHBOARD DATA")
print("=" * 60)

# Prepare data for dashboard
dashboard_data = {
    'summary': {
        'total_patients': int(total_patients),
        'avg_stay': round(float(avg_length_stay), 1),
        'avg_cost': round(float(avg_cost), 2),
        'success_rate': round(float(success_rate), 1),
        'readmission_rate': round(float(readmission_rate), 1)
    },
    'by_condition': condition_stats.reset_index().to_dict('records'),
    'by_treatment': treatment_stats.reset_index().to_dict('records'),
    'by_age_group': age_analysis.reset_index().to_dict('records'),
    'monthly_trends': [
        {'month': str(idx), 'admissions': int(row['Admissions']), 'avg_cost': round(float(row['Avg_Cost']), 2)}
        for idx, row in monthly_trends.iterrows()
    ]
}

# Save to JSON for dashboard
with open('analysis_results.json', 'w') as f:
    json.dump(dashboard_data, f, indent=2)

print("✅ Analysis complete! Results saved to 'analysis_results.json'")

# ==================== STEP 12: KEY RECOMMENDATIONS ====================
print("\n" + "=" * 60)
print("💡 ACTIONABLE RECOMMENDATIONS")
print("=" * 60)

print(f"""
1. 🎯 FOCUS ON {worst_condition.upper()}
   • Success rate is lowest at {condition_stats.loc[worst_condition, 'Success_Rate']:.1f}%
   • Review treatment protocols and consider specialist consultation
   
2. 💰 COST REDUCTION STRATEGY
   • {most_expensive} has highest average cost (${condition_stats.loc[most_expensive, 'Avg_Cost']:,.2f})
   • Consider preventive care programs to reduce acute cases
   
3. 📅 RESOURCE ALLOCATION
   • {len(expensive_long_stay)} patients require extended, expensive care
   • Implement early intervention programs
   
4. 🔄 REDUCE READMISSIONS
   • Current readmission rate: {readmission_rate:.1f}%
   • Strengthen discharge planning and follow-up care
   
5. 📊 LEVERAGE SUCCESSFUL TREATMENTS
   • {best_condition} shows {condition_stats.loc[best_condition, 'Success_Rate']:.1f}% success rate
   • Apply best practices to other conditions
""")

print("=" * 60)
print("Analysis complete! Ready for visualization.")
print("=" * 60)
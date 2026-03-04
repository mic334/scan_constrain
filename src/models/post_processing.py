import os
import pandas as pd
import matplotlib.pyplot as plt 


#print(os.path.exists("data/solvatation_TPrA/steps/energia.dat"))

# legge energia.dat usando spazi multipli come separatore
df_done = pd.read_csv("data/solvatation_TPrA/steps/energia.dat",sep=r'\s+', header=None)
df_error = pd.read_csv("data/solvatation_TPrA/steps/energia_incompleta.dat",sep=r'\s+', header=None)
#print(df.head())


df_done_clean = df_done[[0,6]].copy()
df_error_clean = df_error[[0,6]].copy()
df_done_clean.columns = ['step', 'energy']
df_error_clean.columns = ['step', 'energy']
#fa un sort prima di plottare

df_done_clean = df_done_clean.sort_values(by='step', ascending=True )
df_error_clean = df_error_clean.sort_values(by='step', ascending=True )

df_done_clean['energy in kcal'] = df_done_clean['energy'] * 627.5095
df_error_clean['energy in kcal'] = df_error_clean['energy'] * 627.5095
#print(df_done_clean.head(35))
plt.plot(df_done_clean['step'], df_done_clean['energy in kcal'],marker='x', linestyle='-', label='Done', color='blue') 
plt.plot(df_error_clean['step'], df_error_clean['energy in kcal'],marker='o', linestyle='-', label='Error', color='red')
plt.xlabel('Step')
plt.ylabel('Energy (kcal/mol)')
plt.title('Energy vs Step for Done and Error')
plt.grid()
plt.legend()
plt.savefig("data/solvatation_TPrA/steps/energy_vs_step.png", transparent=True, dpi=300, bbox_inches='tight')  # Salva la figura con una risoluzione di 300 dpi
plt.show()
plt.close()
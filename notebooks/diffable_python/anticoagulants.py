# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# This notebook conatins medicines classed as "anticoagulants". This can be dividied into 
#
# - [All anticoagulant preparations](#all)
# - [Parenteral anticoagulants](#inj) ---> [Current prescribing](https://openprescribing.net/bnf/020801/)
# - [Oral anticoagulants](#oac) ---> [Current prescribing](https://openprescribing.net/bnf/020802/)
#    - [Warfarin](#warf) ---> [Current prescribing](https://openprescribing.net/chemical/0208020V0/)
#    - [DOACs](#doac) ---> [Current prescribing measure as a proprotion on OpenPrescribing](https://openprescribing.net/measure/doacs/national/england/)
# - Other
#
#

#import libraries
from ebmdatalab import bq
import os
import pandas as pd

# ## All anticoagulants preparations  <a id='all'></a>
#
# Jump to:
# - All anticoagulant preparations (this section)
# - [Parenteral anticoagulants](#inj)
# - [Oral anticoagulants](#oac)
#    - [Warfarin](#warf) 
#    - [DOACs](#doac) 

# +
sql = '''WITH bnf_codes AS (
  SELECT bnf_code, chemical FROM hscic.presentation p
  LEFT JOIN (SELECT DISTINCT chemical, chemical_code FROM `ebmdatalab.hscic.bnf`) bnf ON SUBSTR(p.bnf_code,1,9)=bnf.chemical_code
  WHERE 
  bnf_code LIKE '0208%'  #BNF section anticoagulants
)

SELECT "vmp" AS type, id, v.bnf_code, nm, b.chemical
FROM dmd.vmp v
INNER JOIN bnf_codes b ON v.bnf_code=b.bnf_code

UNION ALL

SELECT "amp" AS type, id, a.bnf_code, descr, b.chemical
FROM dmd.amp a
INNER JOIN bnf_codes b ON a.bnf_code=b.bnf_code

ORDER BY type, nm, bnf_code, id'''

complete_anticoagulant_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','complete_anticoagulant_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
complete_anticoagulant_codelist
# -

# ## Parenteral  <a id='inj'></a>
#
# Jump to:
# - [All anticoagulant preparations](#all)
# - Parenteral anticoagulants (this section)
# - [Oral anticoagulants](#oac)
#    - [Warfarin](#warf) 
#    - [DOACs](#doac) 

parenteral_anticoagulant_codelist = complete_anticoagulant_codelist.loc[complete_anticoagulant_codelist["bnf_code"].str[:7]=="0208010"]
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
parenteral_anticoagulant_codelist.reset_index()

parenteral_anticoagulant_codelist.to_csv(os.path.join('..','data','parenteral_anticoagulant_codelist.csv')) 

# ## Oral Anticoagulants  <a id='oac'></a>
#
# Jump to:
# - [All anticoagulant preparations](#all)
# - [Parenteral anticoagulants](#inj)
# - Oral anticoagulants (this section)
#    - [Warfarin](#warf) 
#    - [DOACs](#doac) 

# +
sql = '''WITH bnf_codes AS (
  SELECT bnf_code, chemical FROM hscic.presentation p
  LEFT JOIN (SELECT DISTINCT chemical, chemical_code FROM `ebmdatalab.hscic.bnf`) bnf ON SUBSTR(p.bnf_code,1,9)=bnf.chemical_code
  WHERE 
  bnf_code LIKE '0208020%'  #BNF section anticoagulants - oral
)

SELECT d.*, b.chemical
FROM measures.dmd_objs_with_form_route d
INNER JOIN bnf_codes b ON d.bnf_code=b.bnf_code
WHERE
obj_type IN ('vmp', 'amp')
AND
form_route LIKE '%.oral%' 
ORDER BY obj_type, bnf_code, snomed_id'''


oral_anticoagulant_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','oral_anticoagulant_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
oral_anticoagulant_codelist
# -

# ## Warfarin <a id='warf'></a>
#
# Jump to:
# - [All anticoagulant preparations](#all)
# - [Parenteral anticoagulants](#inj)
# - [Oral anticoagulants](#oac)
#    - Warfarin (this section)
#    - [DOACs](#doac) 

# +
warfarin_codelist = complete_anticoagulant_codelist.loc[complete_anticoagulant_codelist["bnf_code"].str[:9]=="0208020V0"]
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
warfarin_codelist.reset_index(drop=True)


# -

warfarin_codelist.to_csv(os.path.join('..','data','warfarin_codelist.csv')) 

# ## DOACs  <a id='doac'></a>
#
# Jump to:
# - [All anticoagulant preparations](#all)
# - [Parenteral anticoagulants](#inj)
# - [Oral anticoagulants](#oac)
#    - [Warfarin](#warf) 
#    - DOACs (this section)

doac_codelist = complete_anticoagulant_codelist.loc[complete_anticoagulant_codelist["bnf_code"].str[:9].isin(["0208020Z0","0208020X0","0208020AA","0208020Y0"])]
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
doac_codelist.reset_index(drop=True)

doac_codelist.to_csv(os.path.join('..','data','doac_codelist.csv')) 

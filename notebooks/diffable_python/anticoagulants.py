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

# +
sql = '''WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
bnf_code LIKE '0208%'  #BNF section anticoagulants
)

SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, nm, bnf_code, id'''

complete_anticoagulant_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','complete_anticoagulant_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
complete_anticoagulant_codelist
# -

# ## Parenteral  <a id='inj'></a>

# +
sql = '''WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
bnf_code LIKE '0208010%'  #BNF section anticoagulants - parenteral
)

SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, nm, bnf_code, id'''

parenteral_anticoagulant_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','parenteral_anticoagulant_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
parenteral_anticoagulant_codelist
# -

# ## Oral Anticoagulants  <a id='oac'></a>
#
#

# +
sql = '''WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
bnf_code LIKE '0208020%'  #BNF section anticoagulants - oral
)

SELECT *
FROM measures.dmd_objs_with_form_route
WHERE bnf_code IN (SELECT * FROM bnf_codes) 
AND 
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

# +
sql = '''WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
bnf_code LIKE '0208020V0%'  #BNF section anticoagulants - warfarin
)

SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, nm, bnf_code, id'''

wafarin_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','wafarin_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
wafarin_codelist


# -

# ## DOACs  <a id='doac'></a>

# +
sql = '''WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
bnf_code LIKE '0208020Z0%'  OR  #BNF section anticoagulants - apixaban
bnf_code LIKE '0208020X0%'  OR  #BNF section anticoagulants - dabigatran
bnf_code LIKE '0208020AA%'  OR  #BNF section anticoagulants - edoxaban
bnf_code LIKE '0208020Y0%'      #BNF section anticoagulants - rivarxaban

)

SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, nm, bnf_code, id'''

doac_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','doac_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
doac_codelist
# +



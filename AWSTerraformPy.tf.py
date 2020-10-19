import openpyxl as xl
import sys
from terraformpy import Provider, Resource

# excel_file = sys.argv[1]

wb=xl.load_workbook("aws_info.xlsx",data_only=True)

sheet1 = wb['AWS instances']
cells1 = sheet1['A2' : 'G100']

sheet2 = wb['AWS Security Group']
cells2 = sheet2['A2' : 'H100']

sheet3 = wb['Ingress | Egress']
cells3 = sheet3['A2' : 'F100']

sheet4 = wb['SSH Key']
cells4 = sheet4['A2' : 'c100']

sheet5 = wb['Provider']
cells5 = sheet5['A2' : 'c25']

aws_instances = {}
aws_security_groups = {}
Ing_Eg = {}
SSH_Keys = {}
Providers = {}

for a, b, c, d, e, f, g in cells1:
    if a.value != " " and a.value != "" and a.value != None:
        aws_instances[a.value] = [b.value,c.value,d.value,e.value,f.value,g.value]
    else:
        break

for a, b, c, d, e, f, g, h in cells2:
    if a.value != " " and a.value != "" and a.value != None:
        aws_security_groups[a.value] = [b.value,c.value,d.value,e.value,f.value,g.value,h.value]
    else:
        break

for a, b, c, d, e, f in cells3:
    if a.value != " " and a.value != "" and a.value != None:
        Ing_Eg[a.value] = [b.value,c.value,d.value,e.value,f.value]
    else:
        break

for a, b, c in cells4:
    if a.value != " " and a.value != "" and a.value != None:
        SSH_Keys[a.value] = [b.value,c.value]
    else:
        break

for a, b, c in cells5:
    if a.value != " " and a.value != "" and a.value != None:
        Providers[a.value] = [b.value,c.value]
    else:
        break

print("AWS Instance:")
print(aws_instances)
print("AWS Security Groups:")
print(aws_security_groups)
print("Ing Eg:")
print(Ing_Eg)
print("SSH Keys:")
print(SSH_Keys)
print("Providers:")
print(Providers)

# for provider in Providers.keys():
#     Provider(
#         'aws',
#         profile = 'default',
#         region = provider,
#         access_key = Providers[provider][0],
#         secret_key = Providers[provider][1]
#     )
#
# for SHHKey in SSH_Keys.keys():
#     privateKey[SHHKey] = tls_private_key(
#
#     )
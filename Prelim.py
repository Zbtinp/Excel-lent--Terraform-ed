import json

import openpyxl as xl
# from terraformpy import Provider, Resource

import terrascript
import terrascript.provider as provider
import terrascript.resource as resource

wb = xl.load_workbook("aws_info.xlsx", data_only=True)

sheet1 = wb['AWS instances']
cells1 = sheet1['A2': 'G100']

sheet2 = wb['AWS Security Group']
cells2 = sheet2['A2': 'H100']

sheet3 = wb['Ingress | Egress']
cells3 = sheet3['A2': 'F100']

sheet4 = wb['SSH Key']
cells4 = sheet4['A2': 'c100']

sheet5 = wb['Provider']
cells5 = sheet5['A2': 'c25']

aws_instances = {}
aws_security_groups = {}
Ing_Eg = {}
SSH_Keys = {}
Providers = {}

for a, b, c, d, e, f, g in cells1:
    if a.value != " " and a.value != "" and a.value is not None:
        aws_instances[a.value] = [b.value, c.value, d.value, e.value, f.value, g.value]
    else:
        break

for a, b, c, d, e, f, g, h in cells2:
    if a.value != " " and a.value != "" and a.value is not None:
        aws_security_groups[a.value] = [b.value, c.value, d.value, e.value, f.value, g.value, h.value]
    else:
        break

for a, b, c, d, e, f in cells3:
    if a.value != " " and a.value != "" and a.value is not None:
        Ing_Eg[a.value] = [b.value, c.value, d.value, e.value, f.value]
    else:
        break

for a, b, c in cells4:
    if a.value != " " and a.value != "" and a.value is not None:
        SSH_Keys[a.value] = [b.value, c.value]
    else:
        break

for a, b, c in cells5:
    if a.value != " " and a.value != "" and a.value is not None:
        Providers[a.value] = [b.value, c.value]
    else:
        break

# print("AWS Instance:")
# print(aws_instances)
# print("AWS Security Groups:")
# print(aws_security_groups)
# print("Ing Eg:")
# print(Ing_Eg)
# print("SSH Keys:")
# print(SSH_Keys)

# for key in SSH_Keys.keys():
#     print(key)
#     print(SSH_Keys[key][0])
#     print(SSH_Keys[key][1])

config = ""

def build_provider(region, access_key, secret_key):
    return 'provider "aws" {\n region = "' + region + '"\n access_key = "' + access_key + '"\n secret_key = "' + secret_key + '" \n } \n \n'

def build_resource(kind, name, *args):
    flag = True
    setup = 'resource "' + kind + '" "' + name + '" { \n '
    for num in args:
        # setup += str(num) + '\n'
        if flag:
            setup += str(num) + ' = '
            flag = False
        else:
            setup += str(num) + ' \n'
    return setup




for provider in Providers.keys():
    config += build_provider(provider, Providers[provider][0], Providers[provider][1]);

for key in SSH_Keys.keys():
    config += build_resource('tls_private_key', 'pemaster', SSH_Keys[key][0], SSH_Keys[key][1])

outfile = open("test.tf", "w+")
outfile.write(config)
outfile.close
